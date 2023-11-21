from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from .forms import LoginForm
from . import views

app_name = "user"
urlpatterns = [
    path("<str:username>", views.profile, name="profile"),
    path("<str:username>/edit", views.edit_profile, name="edit"),
    path("auth/login/", LoginView.as_view(redirect_authenticated_user=True,form_class=LoginForm)),
    path(
        "auth/password_change/",
        PasswordChangeView.as_view(
            template_name="registration/change_password.html",
            success_url=reverse_lazy("post:index"),
        ),
        name="change_password",
    ),
    path("auth/", include("django.contrib.auth.urls")),
    path("auth/signup", views.signup, name="signup"),
]
