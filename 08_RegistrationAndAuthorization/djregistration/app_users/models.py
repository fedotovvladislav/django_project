from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager


class User(AbstractUser):
    phone_validator = RegexValidator(regex=r"^\+?1?\d{8,15}$")

    phone = models.CharField(validators=[phone_validator], max_length=16, blank=True,
                             verbose_name='Номер телефона')
    city = models.CharField(max_length=50, blank=True, verbose_name='Город')

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class NewsModel(models.Model):
    STATUS_CHOICES = [
        (True, 'Активна'),
        (False, 'Не активна')
    ]

    name = models.CharField(validators=[MinLengthValidator(10)], max_length=200, verbose_name='Заголовок')
    description = models.TextField(validators=[MinLengthValidator(200)], max_length=10000, verbose_name='Содержание')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_edit = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    active = models.BooleanField(choices=STATUS_CHOICES, default=False, verbose_name='Статус')
    tags = TaggableManager()

    class Meta:
        ordering = ['-date_create']
        permissions = (
            ('can_publish', 'Может публиковать'),
        )

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
