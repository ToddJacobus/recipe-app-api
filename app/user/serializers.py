from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        # The attrs param gets sent in automatically as part of the 
        # serializer subclass.  This param is a dictionary that includes
        # information about the user.
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            # Send message with response when authentication fails.
            msg = _("Unable to authenticate with provided credentials.")
            # Django rest framework already knows how to handle these
            # errors.  One of the reasons to use a framework!
            raise serializers.ValidationError(msg, code='authentication')

        # Pass back authenticated/unauthenticated user information
        attrs['user'] = user
        return attrs

