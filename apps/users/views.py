from django.contrib.auth import authenticate, get_user_model, login, logout
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import RoleChoices
from apps.users.permissions import IsApprovedAdmin
from apps.users.serializers import LoginSerializer, RegisterSerializer, UserSerializer

# get_user_model() 返回当前生效的 User 模型（即 settings.AUTH_USER_MODEL 指向的模型）。
# 不要直接 from apps.users.models import User，保持解耦。
User = get_user_model()


# === 登录视图 ===
# APIView：DRF 最基础的视图类，适合非 CRUD 的自定义逻辑。
# 这里用 APIView 而非 GenericAPIView，因为登录不涉及查询集和序列化器自动处理，
# 需要完全手写 post() 流程：校验凭据 → 登录成功建立 session → 返回用户信息。
class LoginView(APIView):
    permission_classes = [AllowAny]
    # authentication_classes 置空：确保未登录用户也能访问登录接口，
    # 否则未登录时可能先被认证中间件拦截返回 401
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Django 内置函数 authenticate()：验证用户名密码是否匹配（密码自动对比哈希）
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {'detail': '用户名或密码错误'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # is_active 检查：未激活（注册后未审核）不能登录
        if not user.is_active:
            return Response(
                {'detail': '账户未激活，请等待管理员审核'},
                status=status.HTTP_403_FORBIDDEN,
            )

        # login() 将 user_id 写入 session（加密存储于 django_session 表中），
        # 并生成 session cookie（Set-Cookie: sessionid=xxx），后续请求浏览器自动携带。
        login(request, user)

        return Response(self.get_serializer(user).data)

    # 复用用户展示序列化器，返回完整用户信息，前端可用于显示当前用户身份
    def get_serializer(self, user):
        return UserSerializer(user)


# === 登出视图 ===
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # logout() 清除 session 数据并删除对应的 django_session 记录
        logout(request)
        return Response({'detail': '已退出登录'})


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
            return Response(
                {'detail': '该用户已审核通过'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.is_approved = True
        user.is_active = True  # 审核通过后才能登录
        user.save()
        # self.get_serializer(user).data 把对象序列化为 JSON
        return Response(self.get_serializer(user).data)
