from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.authtoken.models import Token as TokenModel

from authentication.utils import destroy_token_for_user

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None

        jwt_token = self.get_the_token_from_header(jwt_token)  # clean the token

        # Decode the JWT and verify its signature
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except:
            raise ParseError()
        
        
        # Get the user from the database
        username = payload.get('user_identifier')
        if username is None:
            raise AuthenticationFailed('User identifier not found in JWT')

        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        token = payload.get("token")
        try:
            _ = TokenModel.objects.get(key=token, user=user)
        except ObjectDoesNotExist:
            raise AuthenticationFailed('Token Already expired')
        timestamp_now = datetime.now().timestamp()
        exp = payload.get("exp")
        iat = payload.get("iat")
        if not exp or not iat or (int(exp) + int(iat) < timestamp_now):
            destroy_token_for_user(user)
            raise AuthenticationFailed('Token Already expired')
        # Return the user and token payload
        return user, payload

    def authenticate_header(self, request=None):
        return 'Token'

    @classmethod
    def create_jwt(cls, user, token):
        # Create the JWT payload
        payload = {
            'user_identifier': user.username,
            'exp': int((datetime.now() + timedelta(hours=settings.JWT_CONF['TOKEN_LIFETIME_HOURS'])).timestamp()),
            'iat': datetime.now().timestamp(),
            'token': token
        }

        # Encode the JWT with your secret key
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return jwt_token

    def get_the_token_from_header(self, token):
        token = token.replace(self.authenticate_header(), '').replace(' ', '')  # clean the token
        return token