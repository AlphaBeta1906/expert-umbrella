from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from captcha.fields import CaptchaField
from .models import User

class LoginForm(AuthenticationForm):
    captcha = CaptchaField()
    class Meta:
        fields = ("username","password","captcha")

class CreateUserForm(UserCreationForm):
    captcha = CaptchaField()
    email = forms.EmailField(
        max_length=150,
        help_text="valid and unique email",
        required=True,
        label="Email",
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email","captcha")

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("profile", "email", "show_liked_post", "allow_nsfw","show_email")
