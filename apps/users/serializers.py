from rest_framework import serializers

from apps.users.models import User


# === 用户展示序列化器 ===
class UserSerializer(serializers.ModelSerializer):
    # source='get_role_display'：调用模型的 get_role_display() 获取中文角色名
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone', 'role', 'role_display',
            'real_name', 'is_approved', 'is_active', 'date_joined',
        ]
        read_only_fields = ['is_approved', 'is_active', 'date_joined']
