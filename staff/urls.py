from django.urls import path
from .views import StaffDashboardView, StaffAssetsListView, AssetDetailView, ReportAssetView, StaffAssetsRequestView

urlpatterns = [
    path('dashboard/', StaffDashboardView.as_view(), name='staff-dashboard'),
    path('assets/', StaffAssetsListView.as_view(), name='staff-assets'),
    path('requets/', StaffAssetsRequestView.as_view(), name='staff-request'),
    path('assets/<int:pk>/', AssetDetailView.as_view(), name='my-asset-detail'),
    path('assets/<int:pk>/report/', ReportAssetView.as_view(), name='report-asset'),
]
