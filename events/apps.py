from django.apps import AppConfig

# Configuration class for the 'events' application
class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'

    def ready(self):
        from django.contrib.auth.models import User
        from events.models import UserProfile

        # Default admin credentials
        email = 'an.zinchenko@ukma.edu.ua'
        username = 'admin_ann'
        password = 'admin1234'

        try:
            # Check if a user with the same email or username already exists
            if not User.objects.filter(email=email).exists() and not User.objects.filter(username=username).exists():
                # Create superuser if not found
                user = User.objects.create_superuser(username=username, email=email, password=password)
                user.is_active = True
                user.save()

                # Create associated user profile with admin role
                UserProfile.objects.create(user=user, role='admin')

                print("✅ Default admin user created.")
            else:
                print("ℹ️ Default admin user already exists.")
        except Exception as e:
            # Handle any exceptions during user creation
            print(f"⚠️ Failed to create default admin user: {e}")
