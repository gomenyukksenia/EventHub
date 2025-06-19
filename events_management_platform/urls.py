"""
URL configuration for events_management_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from .views import confirm_code
from .views import dashboard, login_page, logut_page, RegisterPage, forgot_page
from . import settings
from events_management_platform.views import whats_on
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views
from events.views import send_new_password
from events.views import settings_page
from django.contrib.auth.views import LoginView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('login/', login_page, name='login'),
    path('logout/', logut_page, name='logout'),
    path('register/', RegisterPage, name='register'),
    path('forgot-password/', auth_views.PasswordResetView.as_view(
    template_name='forgot-password.html'  # ← твій кастомний шаблон
), name='password_reset'),
    path('events/', include('events.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('verify-email/', confirm_code, name='verify-email'),
    path('events/whats-on/', whats_on, name='whats-on'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'), name='password_reset_confirm'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('send-new-password/', send_new_password, name='send-new-password'),
    path('settings/', settings_page, name='user-settings'),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
