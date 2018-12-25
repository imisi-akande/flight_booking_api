from django import forms
from django.contrib.auth.forms import UserChangeForm
from portfolio.models import User


class FastPaceUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class FastPaceUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
