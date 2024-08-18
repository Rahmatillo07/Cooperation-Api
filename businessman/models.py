from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    USER_ROLE_CHOICES = (
        ('businessman', 'Businessman'),
        ('investor', 'Investor')
    )

    company = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    user_role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, verbose_name='Who are you')
    google_location_url = models.URLField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.username


class Chat(models.Model):
    REQUEST_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, related_name='sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='receive', on_delete=models.CASCADE)
    message = models.TextField()
    file = models.FileField(upload_to='files', null=True, blank=True, validators=[
        FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'wmv', 'png', 'jpg'])
    ])
    status = models.CharField(max_length=20, choices=REQUEST_STATUS_CHOICES, default='pending')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user + ' ' + self.to_user


@receiver(post_save, sender=Chat)
def update_chat_status(sender, instance, **kwargs):
    if instance.status == 'pending':
        instance.status = 'accepted'
        instance.save()
