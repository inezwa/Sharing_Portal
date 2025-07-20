from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import StudyMaterial

@receiver(post_save, sender=StudyMaterial)
def notify_admin_on_upload(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'New Material Uploaded',
            f'A new material "{instance.title}" awaits approval.',
            'from@example.com',
            ['admin@example.com'],
            fail_silently=True,
        )