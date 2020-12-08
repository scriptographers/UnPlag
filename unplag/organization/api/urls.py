from django.urls import path

from organization.api.views import (
	registration_view,
	get_profile,
	update_profile,
    join_org,
	)

app_name = 'organization'
urlpatterns = [
    path('makeorg/', registration_view, name='organization-api-register'),
    path('get/<int:pk>/', get_profile, name='organization-api-profile-view'),
    path('update/<int:pk>/', update_profile, name='organization-api-profile-update'),
    path('joinorg/', join_org, name='organization-api-joinorg'),
]