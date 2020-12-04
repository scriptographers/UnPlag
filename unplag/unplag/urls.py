from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from account.api.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('plagsample/', include('plagsample.urls')),

    #REST_FRAMEWORK_URLS
    path('api/plagsample/', include('plagsample.api.urls', 'plagsample-api')),
    path('api/account/', include('account.api.urls', 'account-api')),
    path('api/organization/', include('organization.api.urls', 'organization-api')),

    #JWT_TOKEN_VIEWS
    # Send username and password to get new access and refresh tokens
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain'),
    # Send refresh token to get new access token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                               document_root=settings.MEDIA_ROOT)
    