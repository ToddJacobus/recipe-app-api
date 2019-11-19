from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag

from recipe import serializers


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    # This function gets called automatically when this view is invoked.
    # Here, we define any filters, like authentication filters, to
    # limit results.
    def get_queryset(self):
        """Return objects for the current authenticated user"""
        # This only works because "user" is a tag attribute.
        return self.queryset.filter(user=self.request.user).order_by('-name')
