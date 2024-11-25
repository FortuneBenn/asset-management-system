from django.contrib import admin
from .models import (
    Notification
)

admin.site.site_url = "/admin/"
# Register your models here.
admin.site.register(Notification)
