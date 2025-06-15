from django import forms
from betterforms.multiform import MultiModelForm
from django import forms
from .models import Event, EventImage, EventAgenda
from django import forms
from events_management_platform.views import whats_on

class EventForm(forms.ModelForm):


    class Meta:
        model = Event
        fields = ['category', 'name', 'uid', 'description', 'job_category', 'scheduled_status', 'venue', 'start_date', 'end_date', 'location', 'points', 'maximum_attende', 'status']
        widgets = {
            'start_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class EventImageForm(forms.ModelForm):


    class Meta:
        model = EventImage
        fields = ['image']

class EmailVerificationForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        label="Verification Code",
        widget=forms.TextInput(attrs={'placeholder': 'Enter the code from email'})
    )

class EventAgendaForm(forms.ModelForm):


    class Meta:
        model = EventAgenda
        fields = ['session_name', 'speaker_name', 'start_time', 'end_time', 'venue_name']

        widgets = {
            'start_time': forms.TextInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TextInput(attrs={'class': 'form-control', 'type': 'time'}),
        }


class EventCreateMultiForm(MultiModelForm):
    form_classes = {
        'event': EventForm,
        'event_image': EventImageForm,
        'event_agenda': EventAgendaForm,
    }
    
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
