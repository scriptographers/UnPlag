from rest_framework import serializers

from organization.models import Organization

from django.contrib.auth.models import User

class OrganizationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Organization
		fields = ['id', 'name', 'title', 'date_created']
			