from django.contrib import admin
from .models import (
    User
)

admin.site.site_url = "/admin/"
# Register your models here.
admin.site.register(User)
