from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from users.apps import UsersConfig

from . import views

app_name = UsersConfig.name

urlpatterns = [
    path("me/", views.ManageUserView.as_view(), name="me"),
    path("token/", views.LoginView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("", views.CreateUserView.as_view(), name="create"),
]
