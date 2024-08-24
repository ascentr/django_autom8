from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('celery-test/', views.celery_test),
    path('dataentery/', include('dataentry.urls')),
    path('emails/', include('emails.urls')),
    path('image-compression/', include('image_compression.urls')),
    path('stockanalysis/', include('stockanalysis.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

