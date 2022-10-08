from django.db import models
from django.core.validators import MinLengthValidator


class NewsModel(models.Model):
    name = models.CharField(validators=[MinLengthValidator(10)], max_length=200, verbose_name='Заголовок')
    description = models.TextField(validators=[MinLengthValidator(200)], max_length=10000, verbose_name='Содержание')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_edit = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        ordering = ['-date_create']


class CommentsModel(models.Model):
    user_name = models.CharField(validators=[MinLengthValidator(2)], max_length=20, verbose_name='Имя пользователя')
    comment = models.TextField(validators=[MinLengthValidator(10)], max_length=3000, verbose_name='Текст комментария')
    news = models.ForeignKey('NewsModel', on_delete=models.CASCADE, null=False,
                             related_name='comments', verbose_name='Новость')
