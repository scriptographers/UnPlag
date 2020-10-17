from django.urls import path

from account.api.views import (
	registration_view,
	get_profile,
	# custom_obtain_auth_token,
	)

app_name = 'account'
urlpatterns = [
	# path('login/', custom_obtain_auth_token, name='api-login'),
    path('signup/', registration_view, name='account-api-signup'),
    path('profile/', get_profile, name='account-api-profile-view'),
]