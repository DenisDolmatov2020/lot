from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rest_framework.urls')),
    path('api/tracker/', include('tracker.urls')),
    path('api/lot/', include('lots.urls')),
    path('api/number/', include('number.urls')),
    path('api/my-user/', include('my_user.urls')),
    path('api/rest-auth/', include('rest_auth.urls')),
    path('api/user/', include('djoser.urls')),
    path('api/auth/', include('rest_framework_social_oauth2.urls')),
    path('api/o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

