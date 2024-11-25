from django.db import models
from administration.models import Asset
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from administration.models import Staff

class RepairRequest(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    reported_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('fixed', 'Fixed')
    ])
    technician_notes = models.TextField(blank=True, null=True)
    staff_notes = models.TextField(blank=True, null=True, default="none")
    updated_at = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=RepairRequest)
def send_repair_request_email(sender, instance, created, **kwargs):
    """
    Sends acknowledgment and completion emails based on the repair request status.
    """
    # Get the asset owner (Staff)
    staff = instance.asset.owner  # Assuming the Asset model has an `owner` field pointing to Staff

    if created and instance.status == 'pending':
        # Acknowledgment email for a new repair request
        subject = "Repair Request Acknowledgment"
        message = (
            f"Dear {staff.name} {staff.surname},\n\n"
            f"Your repair request for the asset '{instance.asset.name}' has been received and is now marked as 'Pending'.\n"
            f"Our technicians will address it shortly.\n\n"
            f"Thank you,\nThe UMAMS Team"
        )
        send_email_to_staff(staff.email, subject, message)

    elif not created and instance.status == 'fixed':
        # Completion email when the status changes to 'fixed'
        subject = "Repair Request Completed"
        message = (
            f"Dear {Staff.name} {Staff.surname},\n\n"
            f"The repair request for your asset '{instance.asset.name}' has been completed and is now marked as 'Fixed'.\n"
            f"You may continue using the asset as normal.\n\n"
            f"Thank you,\nThe UMAMS Team"
        )
        send_email_to_staff(staff.email, subject, message)


def send_email_to_staff(to_email, subject, message):
    """
    Helper function to send email to the staff member.
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='umams1200@gmail.com',  # Update with your host email
            recipient_list=[to_email],
        )
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")