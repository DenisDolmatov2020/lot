from django.db import models
from lot.settings import AUTH_USER_MODEL


class Lot(models.Model):
    creator = models.ForeignKey(AUTH_USER_MODEL, related_name='user', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Название', max_length=48)
    description = models.CharField(verbose_name='Описание', max_length=160, blank=True, null=True)
    image = models.ImageField(verbose_name='Основное изображение', upload_to='lot_images/', blank=True, null=True)
    image_two = models.ImageField(verbose_name='Дополнительное фото', upload_to='lot_images/', blank=True, null=True)
    image_three = models.ImageField(verbose_name='Дополнительное фото', upload_to='lot_images/', blank=True, null=True)
    image_four = models.ImageField(verbose_name='Дополнительное фото', upload_to='lot_images/', blank=True, null=True)
    players = models.PositiveSmallIntegerField(verbose_name='Максимальное кол-во участников', default=3)
    winners = models.PositiveSmallIntegerField(verbose_name='Кол-во победилей', default=1, blank=True)
    winners_complete = models.CharField(verbose_name='Winners complete', max_length=32, null=True)
    energy = models.PositiveSmallIntegerField(verbose_name='Первоначальная затрата энергии на один ход', default=1)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name='Дата изменений', auto_now_add=False, auto_now=True)
    start = models.DateTimeField(verbose_name='Дата старта', auto_now_add=False, auto_now=False, null=True)
    free = models.BooleanField(verbose_name='Свободные места', default=True, blank=True)
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
