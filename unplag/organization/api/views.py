from rest_framework import status, generics, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from organization.models import Organization
from organization.api.serializers import OrganizationSerializer

from account.models import Profile

import os
from pytz import timezone


# Make Organization View
@api_view(['POST', ])
def registration_view(request):
    if request.method == 'POST':
        if request.data.get('name', "") == "":
            return Response({"name": "Can't be empty"}, status=status.HTTP_400_BAD_REQUEST)

        num_count = Organization.objects.filter(name=request.data.get('name', "")).count()

        if num_count != 0:
            return Response({"name": "Already Exists"}, status=status.HTTP_400_BAD_REQUEST)

        new_org = Organization(name=request.data.get('name', ""))
        serializer = OrganizationSerializer(new_org, data=request.data)
        data = {}
        if serializer.is_valid():
            temp_org = serializer.save()

            profile = get_object_or_404(Profile, user=request.user)
            profile.organizations.add(temp_org)

            data['response'] = "Successfully Signed Up"
            data['id'] = temp_org.id
            data['name'] = temp_org.name
            data['title'] = temp_org.title
            data['date_created'] = temp_org.date_created.astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
            data['unique_code'] = temp_org.unique_code
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
###################################################################


# Get Organization Details View
@api_view(['GET', ])
def get_profile(request, pk):
    if request.method == "GET":
        org = get_object_or_404(Organization, pk=pk)
        num_count = org.profile_set.filter(user=request.user).count()

        if(num_count == 1):
            data = {}
            data['id'] = org.id
            data['name'] = org.name
            data['title'] = org.title
            data['unique_code'] = org.unique_code
            data['date_created'] = org.date_created.astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")

            members = org.profile_set.all().order_by("user__id")
            data['members'] = [{"id": member.user.id, "username": member.user.username} for member in members]

            pastchecks = org.plagsamp_set.all().order_by("-date_posted")
            data['pastchecks'] = [{"name": plagsample.name,
                                   "filename": os.path.basename(plagsample.plagzip.name),
                                   "id": plagsample.id,
                                   "timestamp": plagsample.date_posted.astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S"),
                                   } for plagsample in pastchecks]
            return Response(data)
        return Response({"response": "Access Denied"}, status=status.HTTP_403_FORBIDDEN)
###################################################################

# Update Organization Details View


@api_view(['PUT', ])
def update_profile(request, pk):
    if request.method == "PUT":
        org = get_object_or_404(Organization, pk=pk)
        num_count = org.profile_set.filter(user=request.user).count()

        if(num_count == 1):
            serializer = OrganizationSerializer(org, data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = serializer.data
                return Response(data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"response": "Access Denied"}, status=status.HTTP_403_FORBIDDEN)
###################################################################

# Join Organization View


@api_view(['POST', ])
def join_org(request):
    if request.method == 'POST':
        find_org = get_object_or_404(Organization, unique_code=request.data.get('unique_code', "ffffff"))

        find_user = User.objects.filter(username=find_org.name).count()
        if find_user != 0:
            return Response({"response": "Access Denied"}, status=status.HTTP_403_FORBIDDEN)

        profile = get_object_or_404(Profile, user=request.user)
        profile.organizations.add(find_org)

        data = {}
        data['response'] = "Successfully Signed Up"
        data['id'] = find_org.id
        data['name'] = find_org.name
        data['title'] = find_org.title
        data['date_created'] = find_org.date_created.astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
        data['unique_code'] = find_org.unique_code

        members = find_org.profile_set.all().order_by("user__id")
        data['members'] = [{"id": member.user.id, "username": member.user.username} for member in members]
        return Response(data)
###################################################################
