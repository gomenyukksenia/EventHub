from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Corporate email address (@ukma.edu.ua)', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))

class ConfirmationCodeForm(forms.Form):
    code = forms.CharField(
        label='Confirmation Code',
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the 6-digit code'})
    )
