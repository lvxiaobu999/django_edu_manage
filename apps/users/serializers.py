from rest_framework import serializers

from apps.users.models import RoleChoices, User


# === 注册序列化器 ===
# ModelSerializer：DRF 提供的便利类，根据 Model 自动生成字段和简单的 create/update 逻辑。
# 适用于字段和模型一一对应的场景，自定义逻辑可覆写 create()/update()。
class RegisterSerializer(serializers.ModelSerializer):
    # 覆写 password 字段：write_only=True 表示序列化输出时不会包含密码（安全考虑）
    password = serializers.CharField(min_length=6, write_only=True)

    # 覆写 email 字段：required=False 表示非必填
    email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role']

    # 字段级校验：方法名必须是 validate_<field_name>
    def validate_role(self, value):
        # RoleChoices.values 返回 {'ADMIN', 'TEACHER', 'STUDENT'}
        if value not in RoleChoices.values:
            raise serializers.ValidationError('无效的角色')
        return value

    # 对象级校验通过后，调用 create() 创建记录
    # create_user 而非 create，因为前者是 AbstractUser 提供的方法，
    # 内部会自动对密码做哈希处理（绝不要明文存密码）
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            # pop('password') 取出密码，避免传入 create_user 两次
            password=validated_data.pop('password'),
            email=validated_data.get('email', ''),
            role=validated_data['role'],
            is_active=False,    # 注册后不能登录
            is_approved=False,  # 管理员审核后才变成 True
        )
        return user


# === 用户展示序列化器 ===
class UserSerializer(serializers.ModelSerializer):
    # source='get_role_display'：调用模型的 get_role_display() 方法获取中文角色名
    # read_only=True：这个字段只输出，不接收输入
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone', 'role', 'role_display',
            'real_name', 'is_approved', 'is_active', 'date_joined',
        ]
        # read_only_fields：客户端传了也会被忽略，由服务端控制
        read_only_fields = ['is_approved', 'is_active', 'date_joined']


# === 审核序列化器 ===
# 不需要传入任何字段，只是触发审核动作，所以用空 Serializer 即可
class ApproveSerializer(serializers.Serializer):
    pass
