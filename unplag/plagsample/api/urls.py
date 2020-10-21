from django.urls import path

from plagsample.api.views import (
	upload_sample,
	download_csv,
	)

app_name = 'plagsample'
urlpatterns = [
	path('upload/', upload_sample, name='plagsample-api-upload'),
	path('download/<int:pk>/', download_csv, name='plagsample-api-download'),
]