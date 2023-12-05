from django.urls import path
from .views import (
    UserRegistrationView,
    UserAuthenticationView,
    UsersShow,
    UserDetailView,
    AdminTokenObtainView
)


urlpatterns = [
    path('admin/obtain/token/', AdminTokenObtainView.as_view(), name='token-admin'),
    path('api/v1/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('api/v1/auth/', UserAuthenticationView.as_view(), name='user-authentication'),

    # Посмотреть всех юзеров только админ
    path('api/v1/all_users/', UsersShow.as_view(), name='users-all'),

    # Изменить профиль может только владалец
    path('api/v1/user_update/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

]


