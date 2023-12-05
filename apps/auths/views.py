from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser
from .serializers import (
    AdminTokenObtainSerializer,
    UserRegistrationSerializer,
    UserAuthSerializer,
    UsersViewSerializer,
    UserUpdateSerializer
)
from .permissions import IsOwner


# ------------------------------------------------
# GET ADMIN TOKEN
class AdminTokenObtainView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminTokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('admin_email')
        password = serializer.validated_data.get('admin_password')

        try:
            admin = CustomUser.objects.get(email=email, is_staff=True)
        except CustomUser.DoesNotExist:
            return Response({"error": "Admin user not found"}, status=status.HTTP_404_NOT_FOUND)

        if not admin.check_password(password):
            return Response({"error": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(admin)
        access_token = str(refresh.access_token)

        return Response({'access_token': access_token})



# ------------------------------------------------
# User registration
class UserRegistrationView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Пользователь с таким email уже существует"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        validated_data['password'] = make_password(validated_data['password'])

        user_ip = request.META.get('REMOTE_ADDR')
        validated_data['ip_address'] = user_ip

        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        tokens = {
            'user_id': user.id,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(tokens, status=status.HTTP_201_CREATED)


# class AuthTokenObtainPairView(TokenObtainPairView):
#     serializer_class = AuthTokenObtainPairSerializer

# ------------------------------------------------
# User authentication
class UserAuthenticationView(APIView):
    serializer_class = UserAuthSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data["tokens"], status=status.HTTP_200_OK)


# ------------------------------------------------
# All users show
class UsersShow(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UsersViewSerializer
    permission_classes = [IsAdminUser]


# ------------------------------------------------
# Update user
class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    
    # Только аутентифицированный юзер и владалец 
    permission_classes = [IsAuthenticated, IsOwner] 

    # GET: метод позволяет просматривать информацию о пользователе.
    # PUT / PATCH: Эти методы позволяют обновлять информацию о пользователе. 
    #   - PUT обновляет все поля объекта, в то время как 
    #   - PATCH позволяет обновить только выбранные поля.
    # DELETE: Этот метод позволяет удалять пользователя.