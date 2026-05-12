from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import UserProfile, RouteReview


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=RouteReview)
def update_rating_on_save(sender, instance, **kwargs):
    instance.route.refresh_rating()


@receiver(post_delete, sender=RouteReview)
def update_rating_on_delete(sender, instance, **kwargs):
    instance.route.refresh_rating()
