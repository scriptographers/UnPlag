from rest_framework import status, generics, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
# from django.utils import timezone

from account.models import Profile
from account.api.serializers import ProfileSerializer, RegistrationSerializer, ChangePasswordSerializer

from plagsample.models import PlagSamp

from organization.models import Organization

import os
from pytz import timezone


# Registration view for signup
@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request):  # For signup
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            profile = get_object_or_404(Profile, user=user)
            org = Organization(name=user.username)
            org.save()

            profile.organizations.add(org)

            data['response'] = "Successfully Signed Up"
            data['username'] = user.username
            data['userid'] = user.id
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
###################################################################


# Extending TokenObtainPairSerializer to get userid and username !
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add extra responses here
        data['username'] = self.user.username
        data['id'] = self.user.id
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
###################################################################


# Get Profile Details view
@api_view(['GET', ])
def get_profile(request):
    if request.method == "GET":
        profile = get_object_or_404(Profile, user=request.user)
        pr_serializer = ProfileSerializer(profile)
        data = pr_serializer.data
        data['username'] = profile.user.username

        orgs = profile.organizations.all().order_by("name")
        data['orgs'] = [{"org_id": org.id, "org_name": org.name} for org in orgs]
        return Response(data)
###################################################################


# Update Profile details view
@api_view(['PUT', ])
def update_profile(request):
    if request.method == "PUT":
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data['username'] = request.user.username
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
###################################################################


# Update Password view
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            if serializer.data.get("new_password") != serializer.data.get("new_password2"):
                raise serializers.ValidationError({'password': 'Passwords Must Match'})
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
###################################################################


# Get Past Plag Checks
@api_view(['GET', ])
def get_pastchecks(request):
    if request.method == 'GET':
        logged_user = request.user
        past_plagchecks = logged_user.plagsamp_set.all().order_by("organization__name", "-date_posted")

        data = {}
        data['pastchecks'] = [{"name": plagsample.name,
                               "filename": os.path.basename(plagsample.plagzip.name),
                               "file_type": plagsample.file_type,
                               "id": plagsample.id,
                               "timestamp": plagsample.date_posted.astimezone(timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S"),
                               "org_id": plagsample.organization.id,
                               "org_name": plagsample.organization.name,
                               } for plagsample in past_plagchecks]

        return Response(data, status=status.HTTP_200_OK)
###################################################################
