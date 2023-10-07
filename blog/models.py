from django.db import models
from django.urls import reverse
from django.utils import timezone

NULLABLE = {'blank': 'True', 'null': 'True'}


class Blog(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='title',
        unique=True
    )
    body = models.TextField(
        max_length=100,
        verbose_name='content',
        **NULLABLE
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name='slug',
        )
    image = models.ImageField(
        verbose_name='image',
        **NULLABLE
    )
    create_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='creation date',
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='is_published',
    )
    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name='view_count'
    )

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'blog'
        verbose_name_plural = 'blogs'
