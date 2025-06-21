from django import forms
from betterforms.multiform import MultiModelForm
from django import forms
from .models import Event, EventImage, EventAgenda
from django import forms
from django.contrib.auth.models import User
from events.models import UserProfile


# Form: creating or editing events
class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['category', 'name', 'uid', 'description', 'scheduled_status', 'venue', 'start_date', 'end_date', 'points', 'maximum_attende', 'status']
        widgets = {
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


# Form: uploading an event image
class EventImageForm(forms.ModelForm):

    class Meta:
        model = EventImage
        fields = ['image']


# Form: verifying user's email via a code
class EmailVerificationForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        label="Verification Code",
        widget=forms.TextInput(attrs={'placeholder': 'Enter the code from email'})
    )


# Form: managing event agenda sessions
class EventAgendaForm(forms.ModelForm):


    class Meta:
        model = EventAgenda
        fields = ['session_name', 'speaker_name', 'start_time', 'end_time', 'venue_name']

        widgets = {
            'start_time': forms.TextInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TextInput(attrs={'class': 'form-control', 'type': 'time'}),
        }


# Composite form combining event, image, and agenda forms
class EventCreateMultiForm(MultiModelForm):
    form_classes = {
        'event': EventForm,
        'event_image': EventImageForm,
        'event_agenda': EventAgendaForm,
    }


# Form: user login with email and password fields
class LoginForm(forms.Form):
    email = forms.EmailField(label='Corporate email address (@ukma.edu.ua)', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password'
    }))


# Form: entering confirmation code during verification
class ConfirmationCodeForm(forms.Form):
    code = forms.CharField(
        label='Confirmation Code',
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the 6-digit code'})
    )


# Form: updating user settings, including role
class UserSettingsForm(forms.ModelForm):
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'role']