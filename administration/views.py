from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView
from django.views import View
from django.core.paginator import Paginator
from auth_app.models import User
from .models import Asset, Staff, Office
from django.urls import reverse_lazy
from .forms import AssetForm, StaffForm
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from technician.models import RepairRequest
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView


class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "administration/pages/home/index.html"
    login_url = "/auth/login/"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "admin":
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get new and total users (as before)
        today = timezone.now().date()
        new_users_last_week = []
        total_users_last_week = []
        for i in range(7):
            day = today - timezone.timedelta(days=i)
            new_users_count = User.objects.filter(date_joined__date=day).count()
            total_users_count = User.objects.filter(date_joined__date__lte=day).count()
            new_users_last_week.append(new_users_count)
            total_users_last_week.append(total_users_count)
        context['new_users_last_week'] = new_users_last_week[::-1]
        context['total_users_last_week'] = total_users_last_week[::-1]

        # Fetch reported issues (last 5 issues as an example)
        reported_issues = RepairRequest.objects.select_related('asset').order_by('-reported_date')[:5]
        technicians = User.objects.filter(role="technician")
        context['technicians'] = technicians
        context['reported_issues'] = reported_issues

        # Calculate repair requests statistics
        total_requests = RepairRequest.objects.count()
        if total_requests > 0:
            pending_count = RepairRequest.objects.filter(status='pending').count()
            in_progress_count = RepairRequest.objects.filter(status='in_progress').count()
            fixed_count = RepairRequest.objects.filter(status='fixed').count()

            context['repair_stats'] = {
                'pending': {
                    'count': pending_count,
                    'percentage': round((pending_count / total_requests) * 100, 1)
                },
                'in_progress': {
                    'count': in_progress_count,
                    'percentage': round((in_progress_count / total_requests) * 100, 1)
                },
                'fixed': {
                    'count': fixed_count,
                    'percentage': round((fixed_count / total_requests) * 100, 1)
                },
            }
        else:
            # No requests, set stats to 0
            context['repair_stats'] = {
                'pending': {'count': 0, 'percentage': 0},
                'in_progress': {'count': 0, 'percentage': 0},
                'fixed': {'count': 0, 'percentage': 0},
            }

        return context


class AssetsListView(LoginRequiredMixin, TemplateView):
    template_name = "administration/pages/assets/assets.html"
    login_url = "/auth/login/"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "admin":
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        
        # Fetch all assets
        assets = Asset.objects.all()
        
        # Apply pagination (10 items per page, for example)
        paginator = Paginator(assets, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Add paginated assets to context
        context["page_obj"] = page_obj
        return context

class AssetDetailView(LoginRequiredMixin, DetailView):
    login_url = "/auth/login/"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "admin":
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
    model = Asset
    template_name = "administration/pages/assets/asset_detail.html"
    context_object_name = "asset"

class AssetCreateView(LoginRequiredMixin, CreateView):
    login_url = "/auth/login/"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "admin":
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
    
    model = Asset
    form_class = AssetForm
    template_name = "administration/pages/assets/add_asset.html"
    success_url = reverse_lazy('admin-dashboard')  # Redirect after successful submission

    def form_valid(self, form):
        # Additional processing (if needed)
        return super().form_valid(form)
    
class RepairRequestListView(LoginRequiredMixin, ListView):
    login_url = "/auth/login/"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "admin":
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
    
    model = RepairRequest
    template_name = "administration/pages/requests/request_list.html"
    context_object_name = "requests"
    paginate_by = 10  # Optional: paginate with 10 requests per page

    def get_queryset(self):
        # Customize the query if needed, e.g., order by reported date
        return RepairRequest.objects.select_related('asset').order_by('-reported_date')
    
from django.db.models import Q

class StaffListView(View):
    template_name = "administration/pages/staff/staff_list.html"
    login_url = "/auth/login/"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "admin":
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        search_query = request.GET.get('search', '')  # Get search query from the request
        staff_list = Staff.objects.all()

        # Filter staff based on the search query
        if search_query:
            staff_list = staff_list.filter(
                Q(name__icontains=search_query) | 
                Q(surname__icontains=search_query) | 
                Q(staff_number__icontains=search_query) | 
                Q(status__icontains=search_query)
            )

        # Add pagination
        paginator = Paginator(staff_list, 10)  # Show 10 staff members per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {
            'staff_list': page_obj,
            'page_obj': page_obj,
            'is_paginated': paginator.num_pages > 1,
            'search_query': search_query,
        })

    
class AddStaffView(View):
    login_url = "/auth/login/"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "admin":
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
    def get(self, request):
        form = StaffForm()
        return render(request, "administration/pages/staff/add_staff.html", {"form": form})

    def post(self, request):
        if 'individual_submit' in request.POST:
            # Handle individual form submission
            form = StaffForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Staff member added successfully!")
                return redirect("staff-list")
            else:
                messages.error(request, "Error adding staff member.")
                return render(request, "administration/pages/staff/add_staff.html", {"form": form})

        elif 'bulk_upload' in request.FILES:
            excel_file = request.FILES["bulk_upload"]
            try:
                # Read the Excel file
                data = pd.read_excel(excel_file)
                for _, row in data.iterrows():
                    # Ensure building name and office number exist
                    building_name = row.get("Building", "Unknown")  # Default to "Unknown" if missing
                    office_number = row.get("Office")
                    if not office_number:
                        raise ValueError("Office column is missing in the Excel file")

                    # Get or create the office
                    office, _ = Office.objects.get_or_create(
                        building_name=building_name,
                        office_number=office_number,
                    )

                    # Create the staff member
                    Staff.objects.create(
                        staff_number=row["Staff Number"],
                        name=row["Name"],
                        surname=row["Surname"],
                        national_id=row.get("National ID", None),
                        passport_number=row.get("Passport Number", None),
                        status=row["Status"],
                        email =row["Email"],
                        office=office,
                    )
                messages.success(request, "Bulk upload successful!")
            except Exception as e:
                messages.error(request, f"Error processing bulk upload: {e}")
            return redirect("staff-list")
        
class ViewStaffView(DetailView):
    login_url = "/auth/login/"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "admin":
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
    model = Staff
    template_name = "administration/pages/staff/view_staff.html"
    context_object_name = "staff"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all assets assigned to the staff
        context['assets'] = Asset.objects.filter(owner=self.object)
        return context
    
class EditStaffView(UpdateView):
    login_url = "/auth/login/"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "admin":
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
    model = Staff
    form_class = StaffForm
    template_name = "administration/pages/staff/edit_staff.html"
    success_url = reverse_lazy("staff-list")

class DeleteStaffView(DeleteView):
    login_url = "/auth/login/"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "admin":
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
    model = Staff
    template_name = "administration/pages/staff/confirm_delete.html"
    success_url = reverse_lazy("staff-list")

class TechnicianListView(ListView):
    login_url = "/auth/login/"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "admin":
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)
    model = User
    template_name = "administration/pages/users/technician_list.html"
    context_object_name = "technicians"

    def get_queryset(self):
        return User.objects.filter(role="technician")