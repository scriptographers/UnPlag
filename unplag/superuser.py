from django.contrib.auth.models import User
from account.models import Profile

user = User.objects.get(username='dj')
p = Profile(user=user, nick='dj')
p.save()
