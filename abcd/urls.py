from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movie.urls')),
    path('news/', include('blog.urls')),
    path('eco/', include('eco.urls', namespace='eco')),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)