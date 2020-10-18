from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from plagsample.models import PlagSamp 
from plagsample.api.serializers import PlagSampSerializer

## Upload Plag Sample
@api_view(['POST',])
def upload_sample(request):
    if request.method == "POST":
        plag_post = PlagSamp(user=request.user)
        serializer = PlagSampSerializer(plag_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            ## Process stuff here
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
###################################################################

## Get Past User Plag samples
# @api_view(['GET',])
# def get_samples(request):
# 	if request.method == "GET":
		

# Preliminary Work left :
#
# Downloading dummy csv
# Downloading dummy surface plot
# Getting individual plagsample details
