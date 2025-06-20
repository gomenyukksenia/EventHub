from django.contrib.auth import get_user_model

User = get_user_model()
import pytest
from events.forms import (
    EventForm,
    EventImageForm,
    EventAgendaForm,
    EventCreateMultiForm,
    EmailVerificationForm,
    LoginForm,
    ConfirmationCodeForm
)
from django.core.files.uploadedfile import SimpleUploadedFile
from events.models import EventCategory, JobCategory, Event


# EventForm

# Test: EventForm is valid with all required fields
@pytest.mark.django_db
def test_event_form_valid():
    user = User.objects.create_user(username='testuser', password='12345')
    category = EventCategory.objects.create(
        name="Test",
        priority=1,
        code='123',
        image='',
        status=True,
        created_user=user,
        updated_user=user,
    )
    job_category = JobCategory.objects.create(name="FI")
    form_data = {
        'category': category.id,
        'name': 'Test Event',
        'uid': '123',
        'description': 'Some description',
        'job_category': job_category.id,
        'scheduled_status': 'scheduled',
        'venue': 'Hall A',
        'start_date': '2025-06-25',
        'end_date': '2025-06-26',
        'location': 'Kyiv',
        'points': 10,
        'maximum_attende': 100,
        'status': 'active',
    }
    form = EventForm(data=form_data)
    assert form.is_valid()


# Test: EventForm is invalid if required fields are missing
def test_event_form_invalid_missing_fields():
    form = EventForm(data={})
    assert not form.is_valid()
    assert 'name' in form.errors
    assert 'category' in form.errors


# EventImageForm

# Test: EventImageForm is valid with image provided
@pytest.mark.django_db
def test_event_image_form_valid():
    with open('C:/Users/zinch/PycharmProjects/event_hub/images/create_event.png', 'rb') as f:
        image = SimpleUploadedFile('create_event.png', f.read(), content_type='image/png')
    form = EventImageForm(files={'image': image})
    assert form.is_valid(), form.errors


# Test: EventImageForm is invalid without image
def test_event_image_form_invalid():
    form = EventImageForm(data={})
    assert not form.is_valid()
    assert 'image' in form.errors


# EventAgendaForm

# Test: EventAgendaForm is valid with correct data
def test_event_agenda_form_valid():
    form_data = {
        'session_name': 'Opening Speech',
        'speaker_name': 'John Doe',
        'start_time': '09:00',
        'end_time': '10:00',
        'venue_name': 'Main Hall',
    }
    form = EventAgendaForm(data=form_data)
    assert form.is_valid()


# Test: EventAgendaForm is invalid if time missing
def test_event_agenda_form_invalid_missing_time():
    form_data = {
        'session_name': 'Speech',
        'speaker_name': 'Jane Doe',
        'end_time': '10:00',
        'venue_name': 'Room 101',
    }
    form = EventAgendaForm(data=form_data)
    assert not form.is_valid()
    assert 'start_time' in form.errors


# EmailVerificationForm

# Test: EmailVerificationForm is valid with 6-digit code
def test_email_verification_form_valid():
    form = EmailVerificationForm(data={'code': '123456'})
    assert form.is_valid()


# Test: EmailVerificationForm is invalid with empty code
def test_email_verification_form_invalid_empty():
    form = EmailVerificationForm(data={'code': ''})
    assert not form.is_valid()


# LoginForm

# Test: LoginForm is valid with correct email and password
def test_login_form_valid():
    form_data = {
        'email': 'test@ukma.edu.ua',
        'password': '12345678'
    }
    form = LoginForm(data=form_data)
    assert form.is_valid()


# Test: LoginForm is invalid with incorrect email
def test_login_form_invalid_email_format():
    form_data = {
        'email': 'not-an-email',
        'password': 'pass'
    }
    form = LoginForm(data=form_data)
    assert not form.is_valid()
    assert 'email' in form.errors


# ConfirmationCodeForm

# Test: ConfirmationCodeForm is valid with correct code
def test_confirmation_code_form_valid():
    form = ConfirmationCodeForm(data={'code': '987654'})
    assert form.is_valid()


# Test: ConfirmationCodeForm is invalid if code too long
def test_confirmation_code_form_invalid_long_code():
    form = ConfirmationCodeForm(data={'code': '1234567'})
    assert not form.is_valid()


# Test: ConfirmationCodeForm is invalid if code is missing
def test_confirmation_code_form_invalid_empty():
    form = ConfirmationCodeForm(data={'code': ''})
    assert not form.is_valid()


# EventCreateMultiForm

# Test: EventCreateMultiForm is valid if all forms are valid

@pytest.mark.django_db
def test_event_create_multiform_valid():
    user = User.objects.create_user(username='testuser', password='12345')

    category = EventCategory.objects.create(
        name="Workshop",
        priority=1,
        code='',
        image='',
        status=True,
        created_user=user,
        updated_user=user,
    )
    job_category = JobCategory.objects.create(name="Data Science")

    form_data = {
        'event-category': category.id,
        'event-name': 'DS Bootcamp',
        'event-uid': '456',
        'event-description': 'ML and AI content',
        'event-job_category': job_category.id,
        'event-scheduled_status': 'scheduled',
        'event-venue': 'Room 202',
        'event-start_date': '2025-06-25',
        'event-end_date': '2025-06-26',
        'event-location': 'Kyiv',
        'event-points': 15,
        'event-maximum_attende': 50,
        'event-status': 'active',
        'event_agenda-session_name': 'Intro to AI',
        'event_agenda-speaker_name': 'Alice Smith',
        'event_agenda-start_time': '11:00',
        'event_agenda-end_time': '12:00',
        'event_agenda-venue_name': 'AI Lab',
    }

    with open('C:/Users/zinch/PycharmProjects/event_hub/images/create_event.png', 'rb') as f:
        image = SimpleUploadedFile('create_event.png', f.read(), content_type='image/png')

    form_files = {
        'event_image-image': image
    }

    form = EventCreateMultiForm(data=form_data, files=form_files)
    assert form.is_valid(), form.errors


# Test: start_date > end_date
@pytest.mark.django_db
def test_event_form_invalid_dates():
    user = User.objects.create_user(username='testuser', password='12345')
    category = EventCategory.objects.create(
        name="Test Category",
        priority=1,
        code='C123',
        image='',
        status='active',
        created_user=user,
        updated_user=user,
    )
    job_category = JobCategory.objects.create(name="JobCat")
    form_data = {
        'category': category.id,
        'name': 'Event with invalid dates',
        'uid': 101,
        'description': 'Desc',
        'job_category': job_category.id,
        'scheduled_status': 'scheduled',
        'venue': 'Venue',
        'start_date': '2025-06-27',
        'end_date': '2025-06-25',
        'location': 'Kyiv',
        'points': 10,
        'maximum_attende': 100,
        'status': 'active',
    }
    form = EventForm(data=form_data)
    assert not form.is_valid()
    assert 'start_date' in form.errors or 'end_date' in form.errors


# Test: uid is unique
@pytest.mark.django_db
def test_event_form_uid_uniqueness():
    user = User.objects.create_user(username='testuser', password='12345')
    category = EventCategory.objects.create(
        name="Category1",
        priority=1,
        code='C124',
        image='',
        status='active',
        created_user=user,
        updated_user=user,
    )
    job_category = JobCategory.objects.create(name="JobCat2")

    Event.objects.create(
        category=category,
        name="First Event",
        uid=999,
        description="Desc",
        job_category=job_category,
        scheduled_status='scheduled',
        venue='Venue',
        start_date='2025-06-20',
        end_date='2025-06-21',
        points=10,
        maximum_attende=50,
        status='active',
        created_user=user,
        updated_user=user,
    )

    form_data = {
        'category': category.id,
        'name': 'Second Event',
        'uid': 999,
        'description': 'Desc',
        'job_category': job_category.id,
        'scheduled_status': 'scheduled',
        'venue': 'Venue 2',
        'start_date': '2025-06-22',
        'end_date': '2025-06-23',
        'location': 'Kyiv',
        'points': 10,
        'maximum_attende': 30,
        'status': 'active',
    }
    form = EventForm(data=form_data)
    assert not form.is_valid()
    assert 'uid' in form.errors


# Test: points and maximum_attende > 0
@pytest.mark.django_db
@pytest.mark.parametrize("points, maximum_attende", [
    (0, 10),       # points = 0
    (10, 0),       # maximum_attende = 0
    (-1, 10),      # points < 0
    (10, -5),      # maximum_attende < 0
    (0, 0),        # обидва = 0
])
def test_event_form_points_maximum_attende_positive(points, maximum_attende):
    user = User.objects.create_user(username='testuser', password='12345')
    category = EventCategory.objects.create(
        name="Category2",
        priority=2,
        code='C125',
        image='',
        status='active',
        created_user=user,
        updated_user=user,
    )
    job_category = JobCategory.objects.create(name="JobCat3")

    form_data = {
        'category': category.id,
        'name': 'Event Points Test',
        'uid': 200,
        'description': 'Desc',
        'job_category': job_category.id,
        'scheduled_status': 'scheduled',
        'venue': 'Venue',
        'start_date': '2025-06-20',
        'end_date': '2025-06-21',
        'location': 'Kyiv',
        'points': points,
        'maximum_attende': maximum_attende,
        'status': 'active',
    }
    form = EventForm(data=form_data)
    assert not form.is_valid()
    if points <= 0:
        assert 'points' in form.errors
    if maximum_attende <= 0:
        assert 'maximum_attende' in form.errors


# Test: start_time < end_time
def test_event_agenda_form_invalid_time_order():
    form_data = {
        'session_name': 'Session',
        'speaker_name': 'Speaker',
        'start_time': '12:00',
        'end_time': '11:00',
        'venue_name': 'Venue',
    }
    form = EventAgendaForm(data=form_data)
    assert not form.is_valid()
    assert 'end_time' in form.errors or 'start_time' in form.errors


# Test: required fields are empty
@pytest.mark.parametrize("missing_field", [
    'session_name',
    'speaker_name',
    'start_time',
    'end_time',
    'venue_name',
])
def test_event_agenda_form_required_fields_missing(missing_field):
    form_data = {
        'session_name': 'Session',
        'speaker_name': 'Speaker',
        'start_time': '09:00',
        'end_time': '10:00',
        'venue_name': 'Venue',
    }
    form_data.pop(missing_field)
    form = EventAgendaForm(data=form_data)
    assert not form.is_valid()
    assert missing_field in form.errors
