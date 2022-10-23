from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User


class NewsModel(models.Model):
    STATUS_CHOICES = [
        ('a', 'Активна'),
        ('n', 'Не активна')
    ]

    name = models.CharField(validators=[MinLengthValidator(10)], max_length=200, verbose_name='Заголовок')
    description = models.TextField(validators=[MinLengthValidator(200)], max_length=10000, verbose_name='Содержание')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_edit = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    active = models.BooleanField(max_length=1, choices=STATUS_CHOICES, default='a', verbose_name='Статус')

    class Meta:
        ordering = ['-date_create']

    def __str__(self):
        return f'{self.name}'


class CommentsModel(models.Model):
    user_name = models.CharField(validators=[MinLengthValidator(2)], max_length=20,
                                 verbose_name='Имя пользователя')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                             related_name='comments', verbose_name='Авторизация')
    comment = models.TextField(validators=[MinLengthValidator(10)], max_length=3000,
                               verbose_name='Текст комментария')
    news = models.ForeignKey('NewsModel', on_delete=models.CASCADE, null=False,
                             related_name='comments', verbose_name='Новость')

    def __str__(self):
        return f'{self.user_name}: {self.comment[:15]}...'
