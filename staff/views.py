from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView
from administration.models import Asset 
from technician.models import RepairRequest 
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from auth_app.models import User

class StaffDashboardView(TemplateView):
    template_name = "staff/pages/home/index.html"

    def get_context_data(self, **kwargs):
        """Provide dynamic context for the staff dashboard."""
        context = super().get_context_data(**kwargs)
        staff_user = self.request.user  # Get the logged-in user

        # Get the staff record associated with the logged-in user
        try:
            staff = staff_user.staff  # Assuming a OneToOne relationship with the Staff model
        except AttributeError:
            staff = None

        if staff:
            context['logged_in_user'] = staff_user  # Add user details
            context['assigned_assets'] = Asset.objects.filter(owner=staff)  # Assets assigned to the staff
            context['open_requests'] = RepairRequest.objects.filter(
                asset__owner=staff, status__in=['pending', 'in_progress']
            )
            context['issue_count'] = RepairRequest.objects.filter(asset__owner=staff).count()
        else:
            context['logged_in_user'] = staff_user  # Add user details (fallback)
            context['assigned_assets'] = []
            context['open_requests'] = []
            context['issue_count'] = 0

        return context
    
class StaffAssetsListView(TemplateView):
    template_name = "staff/pages/assets/assets.html"

    def get_context_data(self, **kwargs):
        """Provide dynamic context for the staff dashboard."""
        context = super().get_context_data(**kwargs)
        staff_user = self.request.user  # Get the logged-in user

        # Get the staff record associated with the logged-in user
        try:
            staff = staff_user.staff  # Assuming a OneToOne relationship with the Staff model
        except AttributeError:
            staff = None

        if staff:
            context['logged_in_user'] = staff_user  # Add user details
            context['assigned_assets'] = Asset.objects.filter(owner=staff)  # Assets assigned to the staff
            context['open_requests'] = RepairRequest.objects.filter(
                asset__owner=staff, status__in=['pending', 'in_progress']
            )
            context['issue_count'] = RepairRequest.objects.filter(asset__owner=staff).count()
        else:
            context['logged_in_user'] = staff_user  # Add user details (fallback)
            context['assigned_assets'] = []
            context['open_requests'] = []
            context['issue_count'] = 0

        return context
    
class StaffAssetsRequestView(TemplateView):
    template_name = "staff/pages/requests/request_list.html"

    def get_context_data(self, **kwargs):
        """Provide dynamic context for the staff dashboard."""
        context = super().get_context_data(**kwargs)
        staff_user = self.request.user  # Get the logged-in user

        # Get the staff record associated with the logged-in user
        try:
            staff = staff_user.staff  # Assuming a OneToOne relationship with the Staff model
        except AttributeError:
            staff = None

        if staff:
            context['logged_in_user'] = staff_user  # Add user details
            context['assigned_assets'] = Asset.objects.filter(owner=staff)  # Assets assigned to the staff
            context['open_requests'] = RepairRequest.objects.filter(
                asset__owner=staff
            )
            context['issue_count'] = RepairRequest.objects.filter(asset__owner=staff).count()
        else:
            context['logged_in_user'] = staff_user  # Add user details (fallback)
            context['assigned_assets'] = []
            context['open_requests'] = []
            context['issue_count'] = 0

        return context
    
# class AssetDetailView(DetailView):
#     model = Asset
#     template_name = "staff/pages/assets/asset_detail.html"
#     context_object_name = "asset"

class AssetDetailView(DetailView):
    template_name = "staff/pages/assets/asset_detail.html"

    def get(self, request, pk):
        asset = get_object_or_404(Asset, id=pk, owner=request.user.staff)
        unresolved_request = RepairRequest.objects.filter(asset=asset, status__in=['pending', 'in_progress']).exists()
        return render(request, self.template_name, {
            'asset': asset,
            'unresolved_request': unresolved_request
        })

class ReportAssetView(View):
    def post(self, request, pk):
        asset = get_object_or_404(Asset, id=pk, owner=request.user.staff)

        # Check if there is an unresolved repair request for this asset
        unresolved_request = RepairRequest.objects.filter(asset=asset, status__in=['pending', 'in_progress']).exists()

        if unresolved_request:
            messages.error(request, "This asset has already been reported and is awaiting repair.")
            return redirect('my-asset-detail', pk=pk)

        issue_description = request.POST.get('issue_description')

        # Create a new repair request
        RepairRequest.objects.create(
            asset=asset,
            status='pending',
            staff_notes=issue_description
        )
        messages.success(request, "The issue has been reported successfully.")
        return redirect('my-asset-detail', pk=pk)
    
