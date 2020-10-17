from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.contrib.auth.models import User

from plagsample.models import PlagSamp 
from plagsample.api.serializers import PlagSampSerializer


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


# ## Extending TokenObtainPairSerializer to get userid and username !
# class CustomTokenRefreshSerializer(TokenRefreshSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         data['username'] = self.user.username
#         data['id'] = self.user.id
#         return data

# class CustomTokenRefreshView(TokenRefreshView):
#     serializer_class = CustomTokenRefreshSerializer
# ###################################################################


# Login method
# from rest_framework import parsers, renderers
# from rest_framework.authtoken.serializers import AuthTokenSerializer
# from rest_framework.compat import coreapi, coreschema
# from rest_framework.schemas import ManualSchema
# from rest_framework.schemas import coreapi as coreapi_schema
# from rest_framework.views import APIView


# class CustomAuthToken(APIView):
#     authentication_classes = []
#     permission_classes = []

#     throttle_classes = ()
#     parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
#     renderer_classes = (renderers.JSONRenderer,)
#     serializer_class = AuthTokenSerializer

#     if coreapi_schema.is_enabled():
#         schema = ManualSchema(
#             fields=[
#                 coreapi.Field(
#                     name="username",
#                     required=True,
#                     location='form',
#                     schema=coreschema.String(
#                         title="Username",
#                         description="Valid username for authentication",
#                     ),
#                 ),
#                 coreapi.Field(
#                     name="password",
#                     required=True,
#                     location='form',
#                     schema=coreschema.String(
#                         title="Password",
#                         description="Valid password for authentication",
#                     ),
#                 ),
#             ],
#             encoding="application/json",
#         )

#     def get_serializer_context(self):
#         return {
#             'request': self.request,
#             'format': self.format_kwarg,
#             'view': self
#         }

#     def get_serializer(self, *args, **kwargs):
#         kwargs['context'] = self.get_serializer_context()
#         return self.serializer_class(*args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)

#         data= {}
#         data['userid'] = user.id
#         data['username'] = user.username
#         data['token'] = token.key
#         return Response(data)


# custom_obtain_auth_token = CustomAuthToken.as_view() #Login view

# Preliminary Work left :
#
# Uploading files
# Downloading dummy csv
# Downloading dummy surface plot
# Getting user details
# Getting individual plagsample details
