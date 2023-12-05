from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser


# ------------------------------------------------
class AdminTokenObtainSerializer(serializers.Serializer):
    admin_email = serializers.EmailField()
    admin_password = serializers.CharField(write_only=True)


# ------------------------------------------------
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'name', 'surname', 'father_name', 'phone', 'avatar', 'birth_date')


# ------------------------------------------------
class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = CustomUser.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Неверные учетные данные")

        refresh = RefreshToken.for_user(user)
        data["tokens"] = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return data
    
    
# ------------------------------------------------
# 
class UsersViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'name', 'surname', 'phone', 'avatar', 'created_date')


class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = '__all__'