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

        if User.objects.filter(username=uname).exists():
            messages.error(request, "This username is already taken.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect('register')

        if not email.endswith('@ukma.edu.ua'):
            messages.error(request, "Only @ukma.edu.ua email addresses are allowed.")
            return redirect('register')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Створюємо користувача (неактивного)
        my_user = User.objects.create_user(uname, email, pass1)
        my_user.is_active = False
        my_user.save()
        role = 'admin' if email == 'd.svirina@ukma.edu.ua' else request.POST.get('role')  # 'buddy' або 'student'
        UserProfile.objects.create(user=my_user, role=role)

        

        # Генеруємо код підтвердження
        code = str(random.randint(100000, 999999))
        EmailConfirmation.objects.create(user=my_user, code=code)

        # Надсилаємо код
        send_mail(
            'Confirm your email for EventHub',
            f'Your confirmation code is: {code}',
            'noreply@eventhub.test',  # заміни на свою email-адресу при потребі
            [email],
            fail_silently=False
        )

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
        # Add logic later
        pass
    return render(request, 'forgot-password.html')


# ==== Optional old logout (можеш видалити, якщо не потрібно) ====
def logut_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def whats_on(request):
    upcoming_events = Event.objects.filter(end_date__gte=timezone.now()).order_by('start_date')
    context = {
        'events': upcoming_events
    }
    return render(request, 'events/whats_on.html', context)