from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls', namespace = 'blog')),
    path('account/', include('accounts.urls', namespace='accounts')),
    path('account/', include('django.contrib.auth.urls')),
    path('services/', include('services.urls', namespace='services')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
