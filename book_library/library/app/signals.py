from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(user=user)



@receiver(post_delete, sender=User)
def delete_profile(sender, instance, **kwargs):
    user = instance
    try:
        user.profile.delete()
    except:
        pass



@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    profile = instance
    profile.user.delete()