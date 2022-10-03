from django.db import models
from django.utils import timezone
from datetime import timedelta


class Advertisement(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.CharField(max_length=1000, verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    date_start = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    date_cancel = models.DateTimeField(default=timezone.now() + timedelta(days=30),
                                       verbose_name='Дата окончания публикации')
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=False,
                               related_name='advertisements',
                               verbose_name='Автор публикации')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=False,
                                 related_name='advertisements',
                                 verbose_name='Категория')
    adv_type = models.ForeignKey('AdvertisementType', on_delete=models.CASCADE,
                                 default=None, null=True,
                                 related_name='advertisements',
                                 verbose_name='Тип объявления')
    count_views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=20, verbose_name='Имя')
    email = models.CharField(max_length=20, verbose_name='E-mail')
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    def __str__(self):
        return self.name


class Category(models.Model):
    category = models.CharField(max_length=100, verbose_name='Категория')

    def __str__(self):
        return self.category


class AdvertisementType(models.Model):
    adv_type = models.CharField(max_length=100, verbose_name='Тип объявления')

    def __str__(self):
        return self.adv_type
