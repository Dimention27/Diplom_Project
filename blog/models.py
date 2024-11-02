from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class New(models.Model):
    image = models.ImageField(upload_to='images', null=True, verbose_name='Картинка')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Содержимое')
    data = models.DateTimeField(default=timezone.now, verbose_name='Дата и время')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'статьи'
        verbose_name_plural = 'статья'
