import logging

from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.auth.serializers import (
    LoginSerializer,
    LogoutSerializer,
    RegisterSerializer,
)
from apps.users.serializers import UserSerializer
from django_edu_manage.common.response import fail, ok

User = get_user_model()
logger = logging.getLogger(__name__)


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        summary='用户登录',
        description='提交用户名和密码，返回 JWT access token 和 refresh token。',
        request=LoginSerializer,
        responses={200: None},
    )
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


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='用户登出',
        description='提交 refresh token，服务端将其加入黑名单使其失效。',
        request=LogoutSerializer,
        responses={200: None},
    )
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


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        summary='刷新 Token',
        description='access token 过期后，用 refresh token 换取新的 access + refresh token。',
        responses={200: None},
    )
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


@extend_schema_view(
    create=extend_schema(summary='用户注册', description='提交用户名、密码、邮箱和角色，创建新用户。默认 is_approved=False 需管理员审核。'),
)
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
