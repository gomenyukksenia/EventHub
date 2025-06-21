from django.contrib import admin
from mapbox_location_field.admin import MapAdmin  # Enables map widget in the admin interface

# Importing models to register in the Django admin panel
from .models import (
    EventCategory,
    Event,
    JobCategory,
    EventJobCategoryLinking,
    EventMember,
    EventUserWishList,
    UserCoin,
)

# Registering models in the Django admin
admin.site.register(EventCategory)
admin.site.register(Event, MapAdmin)
admin.site.register(JobCategory)
admin.site.register(EventJobCategoryLinking)
admin.site.register(EventMember)
admin.site.register(EventUserWishList)
admin.site.register(UserCoin)
