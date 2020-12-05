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

from models.extractutil import unzip, untar, unrar
from models.txt import TxtPlagChecker

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
                serializer.save() # To prevent accidental saves

                data = serializer.data
                data['date_posted'] = plag_post.date_posted.astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
                
                ## We wish to run this stuff in a separate thread
                try:
                    FILE_NAME = os.path.basename(plag_post.plagzip.name)
                    EXT = FILE_NAME[FILE_NAME.rindex(".")+1:]   
                    OUTFILE = FILE_NAME[:FILE_NAME.index(".")]
                    OUT_PATH = os.path.join(MEDIA_ROOT, "outputcsvfiles")
                    BASE_PATH = os.path.join(MEDIA_ROOT, "plagfiles", OUTFILE)
                    FILE_RE = "*.txt"
                    FILE_PATH = os.path.join(MEDIA_ROOT, plag_post.plagzip.name)
                    
                    # print(FILE_NAME)
                    # print(EXT)
                    # print(OUTFILE)
                    # print(OUT_PATH)
                    # print(BASE_PATH)
                    # print(FILE_RE)
                    # print(FILE_PATH)

                    if EXT == "gz":
                        untar(FILE_PATH, BASE_PATH)
                    elif EXT == "zip":
                        unzip(FILE_PATH, BASE_PATH)
                    elif EXT == "rar":
                        unrar(FILE_PATH, BASE_PATH)

                    txtobj = TxtPlagChecker(BASE_PATH, FILE_RE, OUT_PATH, OUTFILE)
                    csv_name = txtobj.run() # Saves the csv inside the plagfiles directory
                    
                    csv_path = os.path.join(MEDIA_ROOT, "outputcsvfiles", csv_name)
                    csv_f = File(open(csv_path, 'r'))
                    plag_post.outfile.save("csv_" + OUTFILE + ".csv", csv_f)
                except:
                    # Won't interrupt the flow of execution, 
                    # but will generate a null outfile
                    # TODO: Make this Fail-safe
                    pass
                
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