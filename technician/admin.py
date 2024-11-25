from django.contrib import admin
from .models import (
    RepairRequest
)

admin.site.site_url = "/admin/"
# Register your models here.
admin.site.register(RepairRequest)
