from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import RepairRequest
from administration.models import Asset, Staff, Office

class TechnicianDashboardView(TemplateView):
    template_name = "technician/pages/home/index.html"

    def get_context_data(self, **kwargs):
        """Provide dynamic context for the technician dashboard."""
        context = super().get_context_data(**kwargs)
        
        # Get unresolved repair requests
        context['pending_requests'] = RepairRequest.objects.filter(status='pending')
        context['in_progress_requests'] = RepairRequest.objects.filter(status='in_progress')
        context['fixed_requests'] = RepairRequest.objects.filter(status='fixed').order_by('-reported_date')[:5]  # Last 5 fixed
        
        return context

class UpdateRepairStatusView(View):
    def post(self, request, pk):
        repair_request = get_object_or_404(RepairRequest, id=pk)

        # Update the status based on the submitted value
        new_status = request.POST.get('status')
        if new_status in ['in_progress', 'fixed']:
            repair_request.status = new_status
            repair_request.save()
            messages.success(request, f"Repair request marked as '{new_status.replace('_', ' ')}'.")
        else:
            messages.error(request, "Invalid status update.")

        return redirect('technician-dashboard')
    
