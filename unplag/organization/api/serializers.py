from rest_framework import serializers

from organization.models import Organization

from django.contrib.auth.models import User

class OrganizationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Organization
		fields = ['id', 'name', 'title', 'date_created']

	# def save(self):
	# 	if self.validated_data.get('name', "") == "":
	# 		raise serializers.ValidationError({'name': 'Cannot be empty'})

	# 	org_exists = Organization.objects.filter(name=self.validated_data['name']).count()
	# 	if(org_exists != 0):
	# 		raise serializers.ValidationError({'name': 'Already exists!'})

	# 	new_org = Organization(name=self.validated_data['name'], title=self.validated_data.get('title', None))
	# 	new_org.save()

	# 	return new_org
			