from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.safestring import mark_safe


class User(AbstractUser):
    phone_validator = RegexValidator(regex=r"^\+?1?\d{8,15}$")

    avatar = models.ImageField(default='default.png', upload_to='images/', verbose_name='Аватар')
    phone = models.CharField(validators=[phone_validator], max_length=16, blank=True,
                             verbose_name='Номер телефона')

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return f'{self.username}'

    def avatar_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % self.avatar.url)


class BlogModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog',
                             verbose_name='Автор')
    description = models.TextField(max_length=10000, verbose_name='Содержание')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_edit = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        ordering = ['-date_create']
        permissions = (
            ('can_publish', 'Может публиковать'),
        )

    def summary_description(self):
        return self.description[:100]


class FilesModel(models.Model):
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE, related_name='photo',
                             verbose_name='Блог')
    file = models.ImageField(upload_to='blogs/', verbose_name='Аватар')

    def file_tag(self):
        return mark_safe('<img src="%s">' % self.file.url)
