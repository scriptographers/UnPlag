from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
	# User
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
	nick = models.CharField(max_length=255, default='', null=True, blank=True)

	def save(self, *args, **kwargs):
		if not self.nick:
			self.nick = self.user.username
		super().save(*args, **kwargs)

	def __str__(self):
		return self.user.username