from django.urls import path
from .views import RegisterView, CustomLoginView, SignOutView, UserProfileUpdateView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),  # View user profile
    path('profile/edit/', UserProfileUpdateView.as_view(), name='profile_edit'),  # Edit user profile  
]
