import logging

from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.auth.serializers import (
    LoginSerializer,
    LogoutSerializer,
    RegisterSerializer,
)
from apps.users.serializers import UserSerializer
from django_edu_manage.common.response import fail, ok

User = get_user_model()
logger = logging.getLogger(__name__)


# === 登录视图 ===
# JWT 认证流程：
#   用户提交用户名密码 → 验证通过 → 返回 access token + refresh token
#   access token：短期有效（默认 30 分钟），用于调用受保护的 API
#   refresh token：长期有效（默认 7 天），用于在 access token 过期后获取新的
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)
        if user is None:
            logger.warning('登录失败: username=%s, 密码错误', username)
            return fail(message='用户名或密码错误', code=1)

        if not user.is_active:
            logger.warning('登录失败: username=%s, 账户未激活', username)
            return fail(message='账户未激活，请等待管理员审核', code=1)

        refresh = RefreshToken.for_user(user)
        logger.info('用户登录成功: user_id=%s, role=%s', user.id, user.role)
        return ok(data={
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })


# === 登出视图 ===
# JWT 无状态，登出靠黑名单：客户端传 refresh token → 服务端将其加入黑名单
# access token 无法主动失效（除非过期），缓解措施是设短有效期（默认 30 分钟）
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data['refresh']
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info('用户登出成功: user_id=%s', request.user.id)
            return ok(message='已退出登录')
        except TokenError:
            return ok(message='已退出登录')


# === Token 刷新视图 ===
# access token 过期后，前端用 refresh token 换新的 access + refresh token
class TokenRefreshView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return fail(message='refresh token 不能为空', code=400,
                        status_code=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            return ok(data={
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
        except TokenError as e:
            logger.warning('Token 刷新失败: %s', e)
            return fail(message='token 无效或已过期', code=401,
                        status_code=status.HTTP_401_UNAUTHORIZED)


# === 注册视图 ===
# CreateAPIView：只处理 POST，内建 serializer.is_valid() → serializer.save()
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
