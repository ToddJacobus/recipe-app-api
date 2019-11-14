from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    # mechanism by which authentication happens...
    authentication_classes = (authentication.TokenAuthentication, )
    # mechanism by which permissions are configured...
    # This configuration allows anyone who is authenticated to use the
    # API.
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        """Retrive and return authentication user"""
        return self.request.user
