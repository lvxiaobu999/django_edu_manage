from rest_framework import serializers

from apps.users.models import RoleChoices, User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role']

    def validate_role(self, value):
        if value not in RoleChoices.values:
            raise serializers.ValidationError('无效的角色')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data.pop('password'),
            email=validated_data.get('email', ''),
            role=validated_data['role'],
            is_active=False,
            is_approved=False,
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone', 'role', 'role_display',
            'real_name', 'is_approved', 'is_active', 'date_joined',
        ]
        read_only_fields = ['is_approved', 'is_active', 'date_joined']


class ApproveSerializer(serializers.Serializer):
    pass
