from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms import CharField, TextInput, EmailInput, EmailField, PasswordInput
from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    username = CharField(
        max_length=16,
        min_length=3,
        required=True,
        widget=TextInput(attrs={"class": "form-control"}),
    )
    email = EmailField(
        max_length=30, required=True, widget=EmailInput(attrs={"class": "form-control"})
    )
    pass1 = CharField(
        label="Password",
        required=True,
        widget=PasswordInput(attrs={"class": "form-control"}),
    )
    pass2 = CharField(
        label="Repeat password",
        required=True,
        widget=PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "pass1", "pass2")


class LoginForm(AuthenticationForm):
    username = CharField(
        max_length=16,
        min_length=3,
        required=True,
        widget=TextInput(attrs={"class": "form-control"}),
    )
    password = CharField(
        required=True, widget=PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ("username", "password")
