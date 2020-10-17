from rest_framework import serializers

from plagsample.models import PlagSamp

from django.contrib.auth.models import User

class PlagSampSerializer(serializers.ModelSerializer):
	class Meta:
		model = PlagSamp
		fields = ['id', 'plagfile', 'userperson',
			'date_posted', 'outfile']
			