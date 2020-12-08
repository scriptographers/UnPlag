from django.urls import path

from plagsample.api.views import (
	upload_sample,
	download_csv,
	get_sample_info,
	)

app_name = 'plagsample'
urlpatterns = [
	path('upload/', upload_sample, name='plagsample-api-upload'),
	path('download/<int:pk>/', download_csv, name='plagsample-api-download'),
	path('info/<int:pk>/', get_sample_info, name='plagsample-api-info'),
]