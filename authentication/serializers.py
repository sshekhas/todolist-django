from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers, exceptions
from django.core.exceptions import ValidationError as DjangoValidationError
from allauth.account.adapter import get_adapter
from rest_framework.fields import SerializerMethodField


class AuthRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=30,
        min_length=4,
    )
    email = serializers.EmailField(required=False)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(
        max_length=30,
        min_length=4,
    )
    last_name = serializers.CharField(
        max_length=30,
        min_length=4,
        required=False
    )

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username


    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data
    
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data['password1'], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
            )
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_username(self, username, password):
        if username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = 'Must include "username" and "password".'
            raise exceptions.ValidationError(msg)

        return user
    

    @staticmethod
    def validate_auth_user_status(user):
        if not user.is_active:
            msg = 'User account is disabled.'
            raise exceptions.ValidationError(msg)


    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = self._validate_username(username, password)

        if not user:
            msg = 'Unable to log in with provided credentials.'
            raise exceptions.ValidationError(msg)


        self.validate_auth_user_status(user)

        attrs['user'] = user
        return attrs
    

class TokenSerializer(serializers.Serializer):
    key = serializers.CharField()


class UserDetailsSerializer(serializers.HyperlinkedModelSerializer):
    name = SerializerMethodField()
    class Meta:
        model = get_user_model()
        fields = "__all__"


    @staticmethod
    def get_name(obj):
        return f"{obj.first_name} {obj.last_name}"

class UsernameSuggestionSerializer(serializers.Serializer):
    message = serializers.CharField(default="")
    success = serializers.BooleanField(default=False)
    suggested_names = serializers.ListField(default=[])
    