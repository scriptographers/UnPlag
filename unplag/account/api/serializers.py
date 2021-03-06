from rest_framework import serializers

from account.models import Profile

from organization.models import Organization

from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ['id', 'user', 'nick']

class RegistrationSerializer(serializers.ModelSerializer):
	password2 = serializers.CharField(style={'input_type' : 'password'}, write_only=True)

	class Meta:
		model = User
		fields = ['id', 'username', 'password', 'password2']
		extra_kwargs = {
			'password': {'write_only':True}
		}

	def save(self):
		org_exists = Organization.objects.filter(name=self.validated_data['username']).count()
		if(org_exists != 0):
			raise serializers.ValidationError({'username': 'Already exists!'})

		user = User(
			username=self.validated_data['username'],
			)

		password = self.validated_data['password']
		password2 = self.validated_data['password2']

		if password != password2 :
			raise serializers.ValidationError({'password': 'Passwords Must Match'})

		user.set_password(password)
		user.save()
		return user

class ChangePasswordSerializer(serializers.Serializer):
	model = User

	"""
	Serializer for password change endpoint.
	"""
	old_password = serializers.CharField(style={'input_type' : 'password'}, 
										required=True)
	new_password = serializers.CharField(style={'input_type' : 'password'}, 
										required=True)
	new_password2 = serializers.CharField(style={'input_type' : 'password'}, 
										required=True)

