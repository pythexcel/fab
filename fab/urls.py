from django.contrib import admin
from django.urls import path, re_path as url, include
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
   path('admin/', admin.site.urls),
   url(r'^', include('fabapp.urls')),
   url(r'^', include('exbrapp.urls')),
   url(r'^', include('fabrapp.urls')),
   url(r'^', include('review.urls')),
   url(r'^api-auth/',include('rest_framework.urls', namespace='rest_framework'))
]
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT)