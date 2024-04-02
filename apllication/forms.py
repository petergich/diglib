from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile, Archive

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):  # Change here
    class Meta:
        model = Profile
        fields = ["account","profile_image"]

class ArchiveForm(forms.ModelForm):  # Change here
    class Meta:
        model = Archive
        fields = ["name", "owner", "description", "file", "preview_image", "type"]

class UserEditForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

