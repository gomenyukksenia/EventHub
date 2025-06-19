from django.apps import AppConfig

class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'

    def ready(self):
        from django.contrib.auth.models import User
        from events.models import UserProfile

        email = 'an.zinchenko@ukma.edu.ua'
        username = 'admin_ann'
        password = 'admin1234'

        try:
            if not User.objects.filter(email=email).exists() and not User.objects.filter(username=username).exists():
                user = User.objects.create_superuser(username=username, email=email, password=password)
                user.is_active = True
                user.save()

                UserProfile.objects.create(user=user, role='admin')

                print("✅ Default admin user created.")
            else:
                print("ℹ️ Default admin user already exists.")
        except Exception as e:
            print(f"⚠️ Failed to create default admin user: {e}")
