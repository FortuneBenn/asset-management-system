from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import AdminDashboardView, ViewStaffView, AssetsListView, AssetCreateView, AssetDetailView, RepairRequestListView, StaffListView, AddStaffView, EditStaffView, DeleteStaffView, TechnicianListView

urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('assets/', AssetsListView.as_view(), name='assets' ),
    path('assets/add/', AssetCreateView.as_view(), name='add-asset'),
    path('assets/<int:pk>/', AssetDetailView.as_view(), name='asset-detail'),
    path('requests/', RepairRequestListView.as_view(), name='request-list'),
    path('staff/', StaffListView.as_view(), name='staff-list'),
    path('staff/add/', AddStaffView.as_view(), name='add-staff'),
    path('<int:pk>/', ViewStaffView.as_view(), name='view-staff'),
    path('<int:pk>/edit/', EditStaffView.as_view(), name='edit-staff'),
    path('<int:pk>/delete/', DeleteStaffView.as_view(), name='delete-staff'),
    path("technicians/", TechnicianListView.as_view(), name="technician-list"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)