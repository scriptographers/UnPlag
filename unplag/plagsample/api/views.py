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

from models.txt import TxtPlagChecker

import os
import queue
import threading
import time
from pytz import timezone


MEDIA_ROOT = settings.MEDIA_ROOT
# THREAD_QUEUE = queue.Queue()
LIST_THREADS = {}


# Upload Plag Sample
@api_view(['POST', ])
def upload_sample(request):
    if request.method == "POST":
        if request.data.get('file_type', None) is None:
            return Response({'file_type': "This field is needed!"}, status=status.HTTP_400_BAD_REQUEST)

        org = get_object_or_404(Organization, pk=request.data.get('org_id', -1))
        num_count = org.profile_set.filter(user=request.user).count()

        if(num_count == 1):
            plag_post = PlagSamp(user=request.user, organization=org)
            serializer = PlagSampSerializer(plag_post, data=request.data)
            if serializer.is_valid():
                serializer.save()  # To prevent accidental saves

                data = serializer.data
                data['date_posted'] = plag_post.date_posted.astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")

                # We wish to run this stuff in a separate thread
                try:
                    FILE_NAME = os.path.basename(plag_post.plagzip.name)
                    EXT = FILE_NAME[FILE_NAME.rindex(".") + 1:]
                    OUTFILE = FILE_NAME[:FILE_NAME.index(".")]
                    OUT_PATH = os.path.join(MEDIA_ROOT, "outputcsvfiles")
                    BASE_PATH = os.path.join(MEDIA_ROOT, "plagfiles", OUTFILE)
                    FILE_RE = "*.{}".format(plag_post.file_type)  # Will this from the choice field
                    FILE_PATH = os.path.join(MEDIA_ROOT, plag_post.plagzip.name)

                    # Call plag checker on a separate thread

                    # print(FILE_NAME)
                    # print(EXT)
                    # print(OUTFILE)
                    # print(OUT_PATH)
                    # print(BASE_PATH)
                    # print(FILE_RE)
                    # print(FILE_PATH)
                    lock = threading.Lock()
                    txtobj = TxtPlagChecker(BASE_PATH, FILE_PATH, FILE_RE,
                                            OUT_PATH, OUTFILE, EXT, plag_post, lock)
                    txtobj.daemon = False
                    txtobj.name = plag_post.id  # Name of the thread
                    LIST_THREADS[plag_post.id] = txtobj
                    txtobj.start()  # Saves the csv inside the plagfiles directory
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
        # Wait till thread has done its job
        if not file.name:
            if pk in LIST_THREADS:
                LIST_THREADS[pk].join()
                LIST_THREADS.pop(pk, None)
            else:
                data['response'] = "Some unknown error happened while processing the csv"
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            plagsample = PlagSamp.objects.get(pk=pk)
            file = plagsample.outfile
        else:
            LIST_THREADS.pop(pk, None)
        ####################################

        if not file.name:
            data['response'] = "Some unknown error happened while processing the csv"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        file_read = file.open(mode='r')
        f = file_read.readlines()
        file_read.close()

        response = HttpResponse(f, content_type='text/csv')
        response['Content-Length'] = file.size
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file.name)
        return response
###################################################################


# Get Sample Info
@api_view(['GET', ])
def get_sample_info(request, pk):
    if request.method == 'GET':
        data = {}
        try:
            plagsample = PlagSamp.objects.get(pk=pk)
            checkuser = plagsample.organization.profile_set.get(user=request.user)
        except (PlagSamp.DoesNotExist, Profile.DoesNotExist):
            data['response'] = "Forbidden or Wrong Primary Key"
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        
        data['id'] = plagsample.id
        data['name'] = plagsample.name
        data['filename'] = os.path.basename(plagsample.plagzip.name)
        data['file_type'] = plagsample.file_type
        data['timestamp'] = plagsample.date_posted.astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
        data['org_id'] = plagsample.organization.id
        data['org_name'] = plagsample.organization.name
        data['uploader_id'] = plagsample.user.id
        data['uploader'] = plagsample.user.username
        
        return Response(data, status=status.HTTP_200_OK)
###################################################################
