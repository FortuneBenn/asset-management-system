from django.db import models
from auth_app.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils.timezone import now
from django.template.loader import render_to_string

class Office(models.Model):
    building_name = models.CharField(max_length=100, blank=True, null=True)  # Allow NULL values
    office_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.building_name} - {self.office_number}"


from django.utils.timezone import now

class Staff(models.Model):
    user = models.OneToOneField('auth_app.User', on_delete=models.CASCADE, blank=True, null=True)
    staff_number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    national_id = models.CharField(max_length=50, blank=True, null=True)
    passport_number = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('not active', 'Not Active')])
    office = models.ForeignKey('administration.Office', on_delete=models.SET_NULL, null=True, blank=True)
    added_date = models.DateTimeField(default=now)  # Default to the current date and time
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} {self.surname}"


@receiver(post_save, sender=Staff)
def send_staff_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to UMAMS"
        from_email = 'umams1200@gmail.com'
        recipient_list = [instance.email]

        # Render the email content from the template
        context = {
            'name': instance.name,
            'surname': instance.surname,
            'staff_number': instance.staff_number,
            'year': now().year,
        }
        html_message = render_to_string('administration/email/staff_welcome_email.html', context)
        
        try:
            send_mail(
                subject,
                message='',  # Plain text version can be left empty if not needed
                from_email=from_email,
                recipient_list=recipient_list,
                html_message=html_message  # Send the HTML version
            )
            print(f"Email sent to {instance.email}")
        except Exception as e:
            print(f"Failed to send email to {instance.email}: {e}")


class Asset(models.Model):
    name = models.CharField(max_length=100)
    university_barcode = models.CharField(max_length=50, unique=True)
    serial_number = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='assets/images/')
    status = models.CharField(max_length=20, choices=[
        ('damaged', 'Damaged'),
        ('good condition', 'Good Condition'),
        ('fixed', 'Fixed'),
        ('missing', 'Missing')
    ])
    owner = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.university_barcode}"
    
@receiver(post_save, sender=Asset)
def send_asset_assignment_email(sender, instance, created, **kwargs):
    """
    Sends an email to the staff when an asset is assigned or reassigned.
    """
    if instance.owner:  # Check if an owner is assigned
        staff = instance.owner
        subject = "Asset Assigned to You"
        message = (
            f"Dear {staff.name} {staff.surname},\n\n"
            f"The following asset has been assigned to you:\n"
            f"Name: {instance.name}\n"
            f"Barcode: {instance.university_barcode}\n"
            f"Serial Number: {instance.serial_number}\n"
            f"Status: {instance.status}\n\n"
            f"Please contact the administration if you have any questions.\n\n"
            f"Thank you,\nThe UMAMS Team"
        )

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email='umams1200@gmail.com',  # Your host email
                recipient_list=[staff.email],  # Email of the assigned staff
            )
            print(f"Email sent to {staff.email}")
        except Exception as e:
            print(f"Failed to send email to {staff.email}: {e}")