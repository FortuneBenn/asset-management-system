from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import DetailView, UpdateView
from .forms import RegistrationForm, LoginForm, UserChangeForm
from administration.models import Staff
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash

User = get_user_model()

class CustomLoginView(LoginView):
    template_name = "auth_app/login.html"
    form_class = LoginForm
    redirect_authenticated_user = False  # Disable automatic redirection

    def get_success_url(self):
        """Redirect user based on their role."""
        user = self.request.user
        if user.role == 'admin':
            return reverse_lazy("admin-dashboard")
        elif user.role == 'staff':
            return reverse_lazy("staff-dashboard")
        elif user.role == 'technician':
            return reverse_lazy("technician-dashboard")
        else:
            return reverse_lazy("login")
        
    def get_success_url(self):
        user = self.request.user
        print(f"Authenticated user: {user.username}, Role: {user.role}")  # Debug log

        if user.role == 'admin':
            print("Redirecting to admin-dashboard")
            return reverse_lazy("admin-dashboard")
        elif user.role == 'staff':
            print("Redirecting to staff-dashboard")
            return reverse_lazy("staff-dashboard")
        elif user.role == 'technician':
            print("Redirecting to technician-dashboard")
            return reverse_lazy("technician-dashboard")

        print("Role not recognized. Redirecting to fallback login.")
        return reverse_lazy("login")  
    
class RegisterView(View):
    template_name = "auth_app/register.html"

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save the User instance
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')  # Get the selected role
            staff_number = form.cleaned_data.get('staff_number')

            try:
                # Associate the User instance with the corresponding Staff instance
                staff = Staff.objects.get(staff_number=staff_number)
                user.role = role  # Assign the selected role
                user.save()

                staff.user = user
                staff.save()

                # Show success message
                messages.success(request, "Registration successful! Please log in.")
                return redirect("login")
            except Staff.DoesNotExist:
                messages.error(request, "Invalid staff number. Registration failed.")
                user.delete()  # Delete the user if staff number is invalid
        else:
            messages.error(request, "Please correct the errors below.")

        return render(request, self.template_name, {'form': form})
    
class SignOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("login"))
    
class UserProfileView(DetailView):
    model = User
    template_name = "auth_app/profile.html"
    context_object_name = "user"

    def get_object(self):
        return self.request.user  # Fetch the current logged-in user

# View for updating user profile
class UserProfileUpdateView(UpdateView):
    model = User
    template_name = "auth_app/profile_edit.html"
    form_class = UserChangeForm  # Pre-built form that handles user profile fields like email, password, etc.
    context_object_name = "user"

    def get_object(self):
        return self.request.user  # Fetch the current logged-in user

    def form_valid(self, form):
        user = form.save()
        # Update the session to keep the user logged in after updating the password
        if 'password' in form.changed_data:
            update_session_auth_hash(self.request, user)  # Prevent user from being logged out after password change

        messages.success(self.request, "Your profile has been updated successfully.")
        return redirect('profile')  # Redirect to the user profile page

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))
    
class StaffProfileView(DetailView):
    model = User
    template_name = "auth_app/staff_profile.html"
    context_object_name = "user"

    def get_object(self):
        return self.request.user  # Fetch the current logged-in user

# View for updating user profile
class StaffProfileUpdateView(UpdateView):
    model = User
    template_name = "auth_app/staff_profile_edit.html"
    form_class = UserChangeForm  # Pre-built form that handles user profile fields like email, password, etc.
    context_object_name = "user"

    def get_object(self):
        return self.request.user  # Fetch the current logged-in user

    def form_valid(self, form):
        user = form.save()
        # Update the session to keep the user logged in after updating the password
        if 'password' in form.changed_data:
            update_session_auth_hash(self.request, user)  # Prevent user from being logged out after password change

        messages.success(self.request, "Your profile has been updated successfully.")
        return redirect('staff_profile')  # Redirect to the user profile page

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))

