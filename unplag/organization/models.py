from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import uuid

def gen_code(string_length=10):
    random = str(uuid.uuid4()) 
    random = random.upper() 
    random = random.replace("-","") # Remove the UUID '-'.
    
    genned_code = random[0:string_length]
    num_count = Organization.objects.filter(unique_code=genned_code).count()
    if(num_count != 0):
        return gen_code()
        
    return genned_code

class Organization(models.Model):
    unique_code = models.CharField(max_length=10, default=gen_code, editable=False, unique=True)
    date_created = models.DateTimeField(auto_now_add = True, verbose_name = "date posted", editable=False)
    name = models.CharField(max_length=50, null=False, blank=False, editable=False, unique=True)
    title = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = "Welcome to our UnPlag Organization! : " + self.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name