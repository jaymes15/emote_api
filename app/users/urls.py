from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from users.apps import UsersConfig

from . import views

router = DefaultRouter()
router.register("", views.AllUserViewset, basename="all_users")


app_name = UsersConfig.name

urlpatterns = [
    path("all/", include(router.urls)),
    path("me/", views.ManageUserView.as_view(), name="me"),
    path("token/", views.LoginView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("", views.CreateUserView.as_view(), name="create"),
]
