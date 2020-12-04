from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import FileExtensionValidator

from organization.models import Organization

import os


class PlagSamp(models.Model):
	name = models.CharField(max_length=255, default='', verbose_name="sample name", null=False, blank=True)
    plagzip = models.FileField(upload_to='plagfiles/', 
							null=False, blank=False, 
							validators=[FileExtensionValidator(['zip','tar','gz','rar'])])
	date_posted = models.DateTimeField(auto_now_add = True, verbose_name = "date posted", editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, editable=False)
	organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default=None, editable=False)
	outfile = models.FileField(upload_to='outputcsvfiles/', null = False, blank = True)
    # ImageField for the surface plot smh // Don't... Let that processing part for frontend

    def __str__(self):
        return os.path.basename(self.plagzip.name)
