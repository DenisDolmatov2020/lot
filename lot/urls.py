from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rest_framework.urls')),
    path('api/tracker/', include('tracker.urls')),
    path('api/lots/', include('lots.urls')),
    path('api/my_user/', include('my_user.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('api/user/', include('djoser.urls')),
    path('auth/', include('rest_framework_social_oauth2.urls')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
