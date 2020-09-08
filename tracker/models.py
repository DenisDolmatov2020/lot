import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from my_user.models import User


class Tracker(models.Model):

    """ Tracker time model """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, auto_now=False)

    now_minutes = models.PositiveSmallIntegerField(verbose_name='Tracking online minutes', default=0)
    now_ready = models.BooleanField(verbose_name='Ready online track on today', default=False)

    day_minutes = models.PositiveSmallIntegerField(verbose_name='Track day minutes', default=0)
    # day_time_success = models.BooleanField(default=False)
    level_minutes = models.PositiveIntegerField(verbose_name='Track level minutes', default=0)
    # level_time_success = models.BooleanField(default=False)

    days_row = models.PositiveSmallIntegerField(verbose_name='Track days in one row time', default=0)
    # days_row_success = models.BooleanField(default=False)
    days_all = models.PositiveSmallIntegerField(verbose_name='Track days all', default=0)
    # days_all_success = models.BooleanField(default=False)
    time = models.DateTimeField(null=True)

    def __str__(self):
        return '%s, %s, %s, %s' % (self.date, self.user, self.day_minutes, self.level_minutes)
