from rest_framework import serializers
from auth_api.models import UserProfile
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != 'password2':
            raise serializers.ValidationError({'error': "Password fields do not match"})
        return attrs

    def create(self, validated_data):
        user = UserProfile.objects.create_user(username=validated_data['username'],
                                               email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['password', 'last_login', 'is_superuser',
                   'is_staff', 'date_joined', 'user_permissions', 'groups', 'is_active']

    def create(self, validated_data):
        raise serializers.ValidationError('Not possible!')
