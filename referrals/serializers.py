from rest_framework import serializers
from .models import User

class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

class AuthCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    auth_code = serializers.CharField(max_length=4)

class InviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)

class UserProfileSerializer(serializers.ModelSerializer):
    invited_users = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('phone_number', 'invite_code', 'activated_invite_code', 'invited_users')

    def get_invited_users(self, obj):
        return [user.phone_number for user in obj.invited_users.all()]
