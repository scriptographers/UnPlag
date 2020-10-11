from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('plagsample/', include('plagsample.urls')),

    #REST_FRAMEWORK_URLS
    path('api/plagsample/', include('plagsample.api.urls', 'plagsample-api')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
