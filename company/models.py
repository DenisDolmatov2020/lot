from django.db import models

# Create your models here.
from my_user.models import User


class Company(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                unique=True,
                                )
    name = models.CharField(verbose_name='Название компании', max_length=48)
    phrase = models.CharField(verbose_name='Лозунг компании', max_length=96, null=True)
    color = models.CharField(verbose_name='Цвет компании', max_length=24, null=True)
    color_type = models.CharField(verbose_name='Оттенок цвета', max_length=24, null=True)
    color_text = models.CharField(verbose_name='Цвет текста компании', max_length=24, null=True)
    count_games = models.PositiveSmallIntegerField(verbose_name='Количество игр', default=0)
    count_rating = models.PositiveSmallIntegerField(verbose_name='Количество отзывов', default=0)
    rating = models.FloatField(verbose_name='Рейтинг отзывов', default=0)
    image = models.ImageField(verbose_name='Лого компании', upload_to='companies_logo/', blank=True, null=True)

    believe = models.PositiveSmallIntegerField(verbose_name='Индекс доверия в процентов', default=0, blank=True)
    create = models.DateField(verbose_name='Дата создания', auto_now_add=True, auto_now=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
