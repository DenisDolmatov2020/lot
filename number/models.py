from django.db import models
from lot.settings import AUTH_USER_MODEL
from django.dispatch import receiver
from django.db.models.signals import post_save
from lots.models import Lot


@receiver(post_save, sender=Lot)
def create_number(sender, instance=None, created=False, **kwargs):
    if created:
        Number.objects.bulk_create(
            [
                Number(lot=instance, num=i)
                for i in range(1, instance.players + 1)
            ],
        )


class Number(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='Owner', null=True)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='Lot')
    num = models.PositiveSmallIntegerField(verbose_name='Number', default=1, blank=True)
    created = models.DateTimeField(verbose_name='Date create', auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name='Date update', auto_now_add=False, auto_now=True)
    won = models.BooleanField(verbose_name='winner', default=False)
