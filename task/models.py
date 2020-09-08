from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
from my_user.models import User


@receiver(post_save, sender=User)
def create_tasks(sender, instance=None, created=False, **kwargs):
    if created:
        print("CREATE TASK FOR USER !")
        Tasks.objects.create(user=instance)


class Tasks(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, unique=True,)
    now_time = models.PositiveSmallIntegerField(verbose_name='Времени в онлайне', default=0)
    now_success = models.BooleanField(verbose_name='Времени в онлайне выполнено', default=False)
    day_time = models.PositiveSmallIntegerField(verbose_name='Времени за день', default=0)
    day_success = models.BooleanField(verbose_name='Времени за день выполнено', default=False)
    level_time = models.PositiveSmallIntegerField(verbose_name='Время за уровень', default=0)
    level_success = models.BooleanField(verbose_name='Времени за уровень выполнено', default=False)

    word = models.CharField(verbose_name='Секретное слово', max_length=32, null=True)


'''
class Task(models.Model):
    title = models.CharField(verbose_name='Название', max_length=32)
    description = models.CharField(verbose_name='Описание', max_length=80, blank=True, null=True)
    finished = models.BooleanField(verbose_name='Завершенность задания', default=False, blank=True)
    energy = models.PositiveSmallIntegerField(verbose_name='Количество энергии', default=1)
    max_level = models.PositiveSmallIntegerField(verbose_name='Максимальный уровень использования', null=True)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, auto_now=False)


class TaskTime(Task):
    in_on_time = models.BooleanField(verbose_name='Подряд или любое', default=False)
    time = models.PositiveSmallIntegerField(verbose_name='Необходимое время в минутах', default=1)


class TaskWord(Task):
    word = models.CharField(verbose_name='Название', max_length=32)

'''