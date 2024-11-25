from django.contrib import admin
from .models import (
    Office,
    Staff,
    Asset
)

admin.site.site_url = "/admin/"
# Register your models here.
admin.site.register(Office)
admin.site.register(Asset)
admin.site.register(Staff)
