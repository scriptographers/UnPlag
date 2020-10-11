from rest_framework import serializers

from plagsample.models import PlagSamp

from django.contrib.auth.models import User

class PlagSampSerializer(serializers.ModelSerializer):
	class Meta:
		model = PlagSamp
		fields = ['id', 'plagfile', 'userperson',
			'date_posted', 'outfile']

class RegistrationSerializer(serializers.ModelSerializer):
	password2 = serializers.CharField(style={'input_type' : 'password'}, write_only=True)

	class Meta:
		model = User
		fields = ['id', 'username', 'password', 'password2']
		extra_kwargs = {
			'password': {'write_only':True}
		}

	def save(self):
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