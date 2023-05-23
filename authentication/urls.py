# authentication/urls.py

from django.urls import path, include
from rest_framework import routers

from authentication.views import (AuthRegistrationView, AuthLoginView, AuthLogOutView, UserDetailsView, UsernameCheckView)


router = routers.DefaultRouter()
router.register("users", UserDetailsView)

urlpatterns = [
    path("register/", AuthRegistrationView.as_view()),
    path("login/", AuthLoginView.as_view()),
    path("logout/", AuthLogOutView.as_view()),
    path("check-username-availability/", UsernameCheckView.as_view()),
    path("", include(router.urls))
]