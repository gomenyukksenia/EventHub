from django import forms
from django.contrib.auth.models import User
from events.models import UserProfile


# Form: user login with email and password
class LoginForm(forms.Form):
    email = forms.EmailField(label='Corporate email address (@ukma.edu.ua)', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))


# Form: confirmation code input for email verification
class ConfirmationCodeForm(forms.Form):
    code = forms.CharField(
        label='Confirmation Code',
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the 6-digit code'})
    )


# Form: user settings update including username and role
class UserSettingsForm(forms.ModelForm):
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'role']