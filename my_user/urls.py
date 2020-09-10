from django.urls import path
from my_user.views import UserCreateView, UserRetrieveUpdateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# UpdateProfileView,

urlpatterns = [
    # path('token/login/', TokenCreateView.as_view(), name='login'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('profile/', UserRetrieveUpdateView.as_view(), name='user_retrieve_update'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('update/<int:pk>/', UpdateProfileView.as_view(), name='MyTokenObtainPairView'),
]
