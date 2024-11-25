from django.urls import path
from .views import TechnicianDashboardView, UpdateRepairStatusView

urlpatterns = [
    path('dashboard/', TechnicianDashboardView.as_view(), name='technician-dashboard'),
    path('update-repair/<int:pk>/', UpdateRepairStatusView.as_view(), name='update-repair-status'),
]
