from django import forms
from .models import Asset
from .models import Staff

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ['user']  # Exclude the `user` field
        
class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'university_barcode', 'serial_number', 'image', 'status', 'owner']
        widgets = {
            'status': forms.Select(choices=[('damaged', 'Damaged'), ('good condition', 'Good Condition'), ('fixed', 'Fixed'), ('missing', 'Missing')]),
        }
