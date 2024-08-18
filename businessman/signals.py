from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Chat


@receiver(post_save, sender=Chat)
def update_chat_status(sender, instance, **kwargs):
    if instance.status == 'pending':
        instance.status = 'accepted'
        instance.save()
