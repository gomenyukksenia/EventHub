import pytest
from events.forms import LoginForm, ConfirmationCodeForm, UserSettingsForm
from django.contrib.auth.models import User


def test_login_form_valid():
    form = LoginForm(data={'email': 'user@ukma.edu.ua', 'password': 'secret123'})
    assert form.is_valid()


def test_login_form_invalid_email():
    form = LoginForm(data={'email': 'invalidemail', 'password': 'secret123'})
    assert not form.is_valid()
    assert 'email' in form.errors


def test_confirmation_code_form_valid():
    form = ConfirmationCodeForm(data={'code': '123456'})
    assert form.is_valid()


def test_confirmation_code_form_too_long():
    form = ConfirmationCodeForm(data={'code': '1234567'})
    assert not form.is_valid()


def test_confirmation_code_form_empty():
    form = ConfirmationCodeForm(data={'code': ''})
    assert not form.is_valid()


@pytest.mark.django_db
def test_user_settings_form_valid():
    user = User.objects.create(username='testuser')
    form = UserSettingsForm(data={'username': 'newuser', 'role': 'student'}, instance=user)
    assert form.is_valid()


@pytest.mark.django_db
def test_user_settings_form_invalid_role():
    user = User.objects.create(username='testuser')
    form = UserSettingsForm(data={'username': 'newuser', 'role': 'invalid_role'}, instance=user)
    assert not form.is_valid()
    assert 'role' in form.errors
