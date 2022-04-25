from django.db.models.signals import post_save
from .models import CustomUser, ShoppingCart
from django.dispatch import receiver


@receiver(post_save, sender=CustomUser)
def create_shopping_card(sender, instance, created, **kwargs):
    if created:
        ShoppingCart.objects.create(
            user=instance
        )
