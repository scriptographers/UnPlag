from django.urls import path

from plagsample.api.views import (
	registration_view,
	# custom_obtain_auth_token,
	)

app_name = 'plagsample'
urlpatterns = [
	# path('login/', custom_obtain_auth_token, name='api-login'),
    path('signup/', registration_view, name='api-signup'),
]