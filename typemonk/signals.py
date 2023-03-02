from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print("inside the signal-1")
        userInstance = UserProfile(user=instance,userName=instance.username,email=instance.email)
        print("inside the signal-1")
        userInstance.save()
        print("inside the signal-1")
