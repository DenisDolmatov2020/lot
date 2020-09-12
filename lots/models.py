from django.db import models
from lot.settings import AUTH_USER_MODEL


class Lot(models.Model):
    creator = models.ForeignKey(AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Название', max_length=48)
    description = models.CharField(verbose_name='Описание', max_length=160, blank=True, null=True)
    image = models.ImageField(verbose_name='Основное изображение', upload_to='lot/', blank=True, null=True)
    players = models.PositiveSmallIntegerField(verbose_name='Кол-во участников', default=3)
    winners = models.PositiveSmallIntegerField(verbose_name='Кол-во победилей', default=1, blank=True)
    energy = models.PositiveSmallIntegerField(verbose_name='Затрата энергии', default=1)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name='Дата изменений', auto_now_add=False, auto_now=True)
    active = models.BooleanField(verbose_name='Активность игры', default=True, blank=True)


class Condition(models.Model):
    lot = models.ForeignKey(Lot, related_name='condition_set', on_delete=models.CASCADE)
    title = models.CharField(max_length=32, default='Youtube')
    link = models.URLField()
    icon = models.CharField(max_length=32, default='cloud')
    color = models.CharField(max_length=16, default='#ffffff')

    subscribe = models.BooleanField(default=False)
    like = models.BooleanField(default=False)
    repost = models.BooleanField(default=False)
    comment = models.BooleanField(default=False)
    # actions = models.ManyToManyField(Action, related_name="actions_set")
