import logging

from django.contrib.auth import authenticate, get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.permissions import IsApprovedAdmin
from apps.users.serializers import (
    LoginSerializer,
    LogoutSerializer,
    RegisterSerializer,
    UserSerializer,
)
from django_edu_manage.common.response import fail, ok

User = get_user_model()
logger = logging.getLogger(__name__)


# === 登录视图 ===
# 从 Session 认证改为 JWT 认证：
#   用户提交用户名密码 → 验证通过 → 返回 access token + refresh token
#   access token：短期有效（默认 30 分钟），用于调用受保护的 API
#   refresh token：长期有效（默认 7 天），用于在 access token 过期后获取新的
#
# 前端收到 token 后存储在 localStorage 或内存中，
# 每次请求在 Authorization 头里带上：Bearer <access_token>
class LoginView(APIView):
    permission_classes = [AllowAny]
    # authentication_classes 置空：登录接口本身不需要认证，跳过全局 JWT 认证
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Django 内置 authenticate()：验证用户名密码是否匹配（自动对比哈希）
        user = authenticate(request, username=username, password=password)
        if user is None:
            logger.warning('登录失败: username=%s, 密码错误', username)
            # 注意：这里不能返回 401，前端约定 401 表示 token 过期需重定向登录页
            # 账号密码错误属于业务错误，HTTP 200 + code=1 让前端直接展示错误信息
            return fail(message='用户名或密码错误', code=1)

        # is_active 检查：未激活（注册后未审核）不能登录
        if not user.is_active:
            logger.warning('登录失败: username=%s, 账户未激活', username)
            return fail(message='账户未激活，请等待管理员审核', code=1)

        # RefreshToken.for_user() 为指定用户生成一对 token：
        #   refresh = RefreshToken() → 包含 access_token 和 refresh_token
        #   refresh.access_token：短期访问令牌（加密后格式为 JWT 三段式）
        #   str(refresh)：长期刷新令牌（也是 JWT，但有效期更长）
        refresh = RefreshToken.for_user(user)

        logger.info('用户登录成功: user_id=%s, role=%s', user.id, user.role)
        return ok(data={
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })


# === 登出视图 ===
# JWT 是无状态的，服务端不存储 token，所以"登出"靠客户端丢弃 token 实现。
# 但 refresh token 有效期较长（默认 7 天），存在泄露后被恶意使用的风险。
#
# 因此启用 token 黑名单机制：
#   客户端登出时传 refresh token → 服务端将其加入黑名单表
#   → 下次即使用这个 refresh token 请求刷新也会被拒绝
#
# 注意：access token 无法主动失效（除非等它过期），这是 JWT 的固有限制。
# 缓解措施：把 access token 有效期设短（默认 30 分钟），风险窗口可控。
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data['refresh']
        try:
            # 将 refresh token 加入黑名单，此后再用该 token 刷新会被拒绝
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info('用户登出成功: user_id=%s', request.user.id)
            return ok(message='已退出登录')
        except TokenError:
            # token 已过期或格式不对，不需要重复加入黑名单
            return ok(message='已退出登录')


# === Token 刷新视图 ===
# access token 过期后（默认 30 分钟），前端用它调用 API 会收到 401。
# 此时前端应用 refresh token 调用此接口，获取新的 access token（和 refresh token）。
#
# ROTATE_REFRESH_TOKENS=True 时：
#   每次刷新都会返回一个新的 access token 和一个新的 refresh token，
#   旧的 refresh token 同时被加入黑名单（BLACKLIST_AFTER_ROTATION=True）
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
# CreateAPIView：只处理 POST 请求，用于创建资源。
# 继承关系：CreateAPIView → CreateModelMixin → GenericAPIView
# 内建了 get/post → serializer.is_valid() → serializer.save() 的标准流程
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    # AllowAny：不检查登录状态，任何人都可调用
    permission_classes = [AllowAny]


# === 待审核用户列表 ===
# ListAPIView：只处理 GET 请求，返回列表。内建分页和序列化。
class PendingUserListView(ListAPIView):
    serializer_class = UserSerializer
    # permission_classes 是列表，所有权限类都必须通过才能访问
    # DRF 的 IsAuthenticated 检查 request.user 是否已登录
    # 使用 JWT 认证后，request.user 由 JWTAuthentication 从 token 解析而来
    # IsApprovedAdmin 是我们自定义的权限类（见 permissions.py）
    permission_classes = [IsAuthenticated, IsApprovedAdmin]

    # 过滤出未审核的用户
    def get_queryset(self):
        return User.objects.filter(is_approved=False)


# === 用户 ViewSet ===
# ModelViewSet 是 DRF 最强大的视图类，它继承了 5 个 Mixin：
#   CreateModelMixin  → POST   /
#   ListModelMixin    → GET    /
#   RetrieveModelMixin→ GET    /{id}/
#   UpdateModelMixin  → PUT    /{id}/
#   DestroyModelMixin → DELETE /{id}/
# 配合 DefaultRouter（见 urls.py），这些路由自动生成。
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsApprovedAdmin]

    # @action 装饰器：在标准 CRUD 之外添加自定义端点
    # detail=True：作用于单个资源，URL 为 /{prefix}/{pk}/approve/
    # detail=False：作用于列表，URL 为 /{prefix}/approve/
    # methods=['post']：只接受 POST 请求
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        # self.get_object() 根据 URL 中的 pk 获取对象
        user = self.get_object()
        if user.is_approved:
            return fail(message='该用户已审核通过', code=400,
                        status_code=status.HTTP_400_BAD_REQUEST)
        user.is_approved = True
        user.is_active = True  # 审核通过后才能登录
        user.save()
        logger.info('管理员审核用户通过: user_id=%s, admin_id=%s', user.id, request.user.id)
        # self.get_serializer(user).data 把对象序列化为 JSON
        return ok(data=self.get_serializer(user).data)
