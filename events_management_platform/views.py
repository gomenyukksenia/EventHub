import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from events.models import UserProfile
from events.models import EventCategory, Event, EmailConfirmation
from .forms import LoginForm, ConfirmationCodeForm  # не забудь створити ConfirmationCodeForm
from events.models import UserProfile
from django.utils import timezone
from django.core.mail import EmailMessage
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


from events.forms import UserSettingsForm


# ==== DASHBOARD ====
@login_required(login_url='login')
def dashboard(request):
    profile = request.user.userprofile
    if profile.role == 'admin':
        context = {
            'user': User.objects.count(),
            'event_ctg': EventCategory.objects.count(),
            'event': Event.objects.count(),
            'complete_event': Event.objects.filter(status='completed').count(),
            'events': Event.objects.all()
        }
        return render(request, 'dashboard.html', context)

    elif profile.role == 'buddy':
        events = Event.objects.filter(created_user=request.user)
        context = {
            'event_ctg': EventCategory.objects.filter(created_user=request.user).count(),
            'event': events.count(),
            'complete_event': events.filter(status='completed').count(),
            'events': events
        }
        return render(request, 'buddy_dashboard.html', context)

    else:
        return render(request, 'student_dashboard.html')


# View: edit event with buddy restrictions
@login_required
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.user.userprofile.role == 'buddy':
        if event.created_user != request.user:
            return HttpResponseForbidden("You can only edit your own events.")
        time_diff = timezone.now().date() - event.created_date
        if time_diff.total_seconds() > 300:
            return HttpResponseForbidden("You can only edit within 5 minutes of creation.")

    # далі — звичайна логіка редагування


# ==== LOGIN ====
def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                return HttpResponse("This email is not registered.")

            if not email.endswith('@ukma.edu.ua'):
                return HttpResponse("This app is only for the Kyiv-Mohyla Academy community.")

            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                return HttpResponse("Incorrect password.")

    return render(request, 'login.html', {'form': form})


# ==== LOGOUT ====
def logout_view(request):
    logout(request)
    return redirect('login')


# ==== REGISTER ====
def RegisterPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        role = request.POST.get('role')

        context = {
            'username': uname,
            'email': email,
            'role': role,
        }

        if User.objects.filter(username=uname).exists():
            messages.error(request, "This username is already taken.")
            return render(request, 'register.html', context)

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'register.html', context)

        if not email.endswith('@ukma.edu.ua'):
            messages.error(request, "Only @ukma.edu.ua email addresses are allowed.")
            return render(request, 'register.html', context)

        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html', context)

        # Створюємо користувача (неактивного)
        my_user = User.objects.create_user(uname, email, pass1)
        my_user.is_active = False
        my_user.save()
        role = 'admin' if email == 'an.zinchenko@ukma.edu.ua' else role
        UserProfile.objects.create(user=my_user, role=role)

        # Генеруємо код підтвердження
        code = str(random.randint(100000, 999999))
        EmailConfirmation.objects.create(user=my_user, code=code)

        # Надсилаємо лист
        email_message = EmailMessage(
            subject='Your EventHub Confirmation Code',
            body=f"""
Hello,

Thank you for registering on EventHub!

Your confirmation code is: {code}

If you didn't request this, please ignore the email.

Best regards,  
EventHub Team
""",
            from_email='EventHub Confirmation <eventhub472@gmail.com>',
            to=[email]
        )
        email_message.send()

        # Зберігаємо ID в сесію
        request.session['pending_user_id'] = my_user.id

        messages.success(request, "Account created! Please check your email for the confirmation code.")
        return redirect('verify-email')

    return render(request, 'register.html')


# ==== VERIFY CODE ====
def confirm_code(request):
    user_id = request.session.get('pending_user_id')
    if not user_id:
        return redirect('register')

    user = User.objects.get(id=user_id)
    confirmation = EmailConfirmation.objects.get(user=user)

    if request.method == 'POST':
        form = ConfirmationCodeForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['code'] == confirmation.code:
                user.is_active = True
                user.save()
                confirmation.is_confirmed = True
                confirmation.save()
                messages.success(request, "Email confirmed. You can now log in.")
                return redirect('login')
            else:
                form.add_error('code', 'Incorrect confirmation code.')
    else:
        form = ConfirmationCodeForm()

    return render(request, 'confirm_code.html', {'form': form})


# ==== FORGOT PASSWORD ====
def forgot_page(request):
    if request.method == 'POST':
        pass
    return render(request, 'forgot-password.html')


def logut_page(request):
    logout(request)
    return redirect('login')


# View: show upcoming events to logged-in users
@login_required(login_url='login')
def whats_on(request):
    upcoming_events = Event.objects.filter(end_date__gte=timezone.now()).order_by('start_date')
    context = {
        'events': upcoming_events
    }
    return render(request, 'events/whats_on.html', context)


# View: send a new password to user's email
def send_new_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponse("This email is not registered.")

        # Генеруємо новий пароль
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        user.set_password(new_password)
        user.save()

        # Надсилаємо новий пароль
        email_message = EmailMessage(
            subject='Your New Password',
            body=f'''
Hi {user.username},

You requested a password reset on EventHub.
Your new password is: {new_password}

You can now log in using this password. For security reasons, please change it after logging in.

Best regards,  
EventHub Team
''',
            from_email='EventHub <eventhub472@gmail.com>',
            to=[email]
        )
        email_message.send()

        return HttpResponse("A new password has been sent to your email.")

    return render(request, 'events/send_new_password.html')


# View: user settings update with password change support
@login_required
def settings_page(request):
    user = request.user
    profile = user.userprofile

    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user)
        current = request.POST.get('current_password')
        new = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')

        if form.is_valid():
            user.username = form.cleaned_data['username']
            profile.role = form.cleaned_data['role']
            profile.save()

            if current and new and confirm:
                if not user.check_password(current):
                    messages.error(request, '❌ Current password is incorrect.')
                elif new != confirm:
                    messages.error(request, '❌ New passwords do not match.')
                else:
                    user.set_password(new)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, '✅ Password updated successfully.')
            else:
                user.save()
                messages.success(request, '✅ Settings updated successfully.')

            return redirect('user-settings')
    else:
        form = UserSettingsForm(instance=user, initial={'role': profile.role})

    return render(request, 'setting-page.html', {'form': form})