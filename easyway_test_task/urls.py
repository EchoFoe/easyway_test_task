from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Easyway API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('travel.urls', namespace='travel')),
]\
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)