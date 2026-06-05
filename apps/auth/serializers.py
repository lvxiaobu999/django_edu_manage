from rest_framework import serializers

from apps.core.choices import RoleChoices
from apps.users.models import User


# === 注册序列化器 ===
# ModelSerializer 根据 Model 自动生成字段和简单的 create/update 逻辑。
# 适用于字段和模型一一对应的场景，自定义逻辑可覆写 create()/update()。
class RegisterSerializer(serializers.ModelSerializer):
    # write_only=True：序列化输出时不会包含密码
    password = serializers.CharField(min_length=6, write_only=True)

    # required=False：非必填
    email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role']

    # 字段级校验：方法名必须是 validate_<field_name>
    def validate_role(self, value):
        if value not in RoleChoices.values:
            raise serializers.ValidationError('无效的角色')
        return value

    # 对象级校验通过后调用 create() 创建记录。
    # create_user 而非 create：前者是 AbstractUser 提供的方法，
    # 内部会自动对密码做哈希处理（绝不要明文存密码）
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data.pop('password'),
            email=validated_data.get('email', ''),
            role=validated_data['role'],
            is_active=False,     # 注册后不能登录
            is_approved=False,   # 管理员审核后才变成 True
        )
        return user


# === 登录序列化器 ===
# 登录不需要 ModelSerializer（不创建/更新数据库记录），
# 只校验用户名和密码是否匹配
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=6, write_only=True)


# === 登出序列化器 ===
# JWT 登出需要前端传入 refresh token，服务端将其加入黑名单使其失效
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text='refresh token，登出后将被加入黑名单')
