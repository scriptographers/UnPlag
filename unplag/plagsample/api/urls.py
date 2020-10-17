from django.urls import path

from plagsample.api.views import (
	upload_sample,
	)

app_name = 'plagsample'
urlpatterns = [
	path('upload/', upload_sample, name='plagsample-api-upload'),
]