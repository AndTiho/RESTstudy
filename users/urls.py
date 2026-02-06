from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import CheckoutSessionStatusView, PaymentListAPIView, PriceCreateAPIView

from .views import UserCreateAPIView, UserDeleteView, UserDetailView, UserListView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path("users/register/", UserCreateAPIView.as_view(), name="user-register"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("users/<int:pk>/update/", UserUpdateView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user-delete"),
    path("users/login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("users/token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
    path("payments/", PaymentListAPIView.as_view(), name="payment_list"),
    path("course/<int:course_id>/pay/", PriceCreateAPIView.as_view(), name="create_payment"),
    path("lesson/<int:lesson_id>/pay/", PriceCreateAPIView.as_view(), name="create_payment"),
    path(
        "stripe/session/<str:session_id>/status/", CheckoutSessionStatusView.as_view(), name="checkout_session_status"
    ),
]
