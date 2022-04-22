from django.contrib import admin

# Register your models here.
from .models import Category, NewsMovie


admin.site.register(Category)
admin.site.register(NewsMovie)
