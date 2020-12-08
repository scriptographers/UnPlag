from django.urls import path

from account.api.views import (
	registration_view,
	get_profile,
	update_profile,
	ChangePasswordView,
	get_pastchecks,
	)

app_name = 'account'
urlpatterns = [
    path('signup/', registration_view, name='account-api-signup'),
    path('profile/', get_profile, name='account-api-profile-view'),
    path('update/', update_profile, name='account-api-profile-update'),
	path('upassword/', ChangePasswordView.as_view(), name='account-api-change-password'),
	path('pastchecks/', get_pastchecks, name='account-api-get-pastchecks')
]