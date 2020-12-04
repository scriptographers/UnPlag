from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.files import File
from django.conf import settings
from django.shortcuts import get_object_or_404

from plagsample.models import PlagSamp
from plagsample.api.serializers import PlagSampSerializer

from organization.models import Organization

from account.models import Profile

import os
from pytz import timezone

MEDIA_ROOT = settings.MEDIA_ROOT


# Upload Plag Sample
@api_view(['POST', ])
def upload_sample(request):
    if request.method == "POST":
        org = get_object_or_404(Organization, pk=request.data.get('org_id', -1))
        num_count = org.profile_set.filter(user=request.user).count()

        if(num_count == 1):
            plag_post = PlagSamp(user=request.user, organization=org)
            serializer = PlagSampSerializer(plag_post, data=request.data)
            if serializer.is_valid():
                serializer.save()

                data = serializer.data
                data['date_posted'] = plag_post.date_posted.astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")

                # Dummy csv for testing
                csv_path = os.path.join(MEDIA_ROOT, "outputcsvfiles/jaccard.csv")
                csv_f = File(open(csv_path, 'r'))
                plag_post.outfile.save("csv_" + os.path.splitext(os.path.basename(plag_post.plagzip.name))[0] + ".csv", csv_f)

                serializer = PlagSampSerializer(plag_post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"response": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
###################################################################


# Download CSV Sample
@api_view(['GET', ])
def download_csv(request, pk):
    if request.method == 'GET':
        user = request.user
        data = {}
        try:
            plagsample = PlagSamp.objects.get(pk=pk)
            num_count = plagsample.organization.profile_set.get(user=request.user)
        except (PlagSamp.DoesNotExist, Profile.DoesNotExist):
            data['response'] = "Forbidden or Wrong Primary Key"
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        file = plagsample.outfile
        file_name = file.name
        if not file_name:
            data['response'] = "Output CSV not processed yet !"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        file_read = file.open(mode='r')
        f = file_read.readlines()
        file_read.close()

        response = HttpResponse(f, content_type='text/csv')
        response['Content-Length'] = file.size
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
        return response
###################################################################

# Preliminary Work left :
#
# Downloading dummy surface plot
# Getting individual plagsample details
