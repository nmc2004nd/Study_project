from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        """
        Tạo user mới. Dùng create_user để tự hash password và 
        đảm bảo các quy trình tạo user mặc định được thực thi.
        """
        return User.objects.create_user(**validated_data)
