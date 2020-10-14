from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

# Create your models here.

class PlagSamp(models.Model):
	plagfile = models.FileField(upload_to='plagfiles/', null=False, blank=False)
	date_posted = models.DateTimeField(auto_now_add = True, verbose_name = "date posted")
	userperson = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	outfile = models.FileField(upload_to='outputcsvfiles/', null = False, blank = True)
	# ImageField for the surface plot smh

	def __str__(self):
		return self.plagfile.filename


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
# 	if created:
# 		Token.objects.create(user=instance)