from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from django.template.defaultfilters import slugify
from django.db.models.aggregates import (Sum)



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'


class NewsMovie(models.Model):
    headline = models.CharField(max_length=250)
    discription = models.TextField()
    image = models.ImageField(upload_to='blogpic')
    date = models.DateTimeField(auto_now_add=True)
    # tags = 
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='categories',
        null=True,
        blank=False)

    def __str__(self):
        return self.headline

    class Meta:
        db_table = ''
        ordering = ('-headline'),
        managed = True
        verbose_name = 'NewsMovie'
        verbose_name_plural = 'NewsMovies'    
