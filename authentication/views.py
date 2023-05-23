
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView

from authentication.utils import create_token_for_user, destroy_token_for_user, get_similer_username
from authentication.serializers import AuthRegistrationSerializer, LoginSerializer, TokenSerializer, UserDetailsSerializer, UsernameSuggestionSerializer
from authentication.authentication import JWTAuthentication
from utils.permissions import IsAdminOrReadAndUpdate

# Create your views here.

class AuthRegistrationView(GenericAPIView):
    serializer_class = AuthRegistrationSerializer
    permission_classes = (AllowAny,)


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        token = create_token_for_user(user)
        jwt_token = JWTAuthentication.create_jwt(user, token.key)
        if token:
            serializer = TokenSerializer(
                data={"key": jwt_token}
            )
            serializer.is_valid(raise_exception=True)
            response = Response(serializer.data, status=status.HTTP_200_OK)
        else:
            response = Response(status=status.HTTP_204_NO_CONTENT)

        return response

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        return user



class AuthLoginView(GenericAPIView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework

    Accept the following POST parameters: username, password
    Return the REST Framework Token Object's key.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    user = None
    access_token = None
    token = None


    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token = create_token_for_user(self.user)
    

    def get_response(self):

        if self.token:
            jwt_token = JWTAuthentication.create_jwt(self.user, self.token.key)
            serializer = TokenSerializer(
                data={"key": jwt_token}
            )
            serializer.is_valid(raise_exception=True)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)

        self.login()
        return self.get_response()
    

class AuthLogOutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)


    def post(self, request, *args, **kwargs):    
        destroy_token_for_user(request.user)
        response = Response(
            {'detail': 'Successfully logged out.'},
            status=status.HTTP_200_OK,
        )
        return response
    

class UserDetailsView(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserDetailsSerializer
    pagination_class = None

    permission_classes = [IsAuthenticated, IsAdminOrReadAndUpdate]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return super().get_queryset().filter(id=self.request.user.id)
        return super().get_queryset()
    

class UsernameCheckView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        user_name = request.query_params.get("username")
        existing = get_user_model().objects.only("username")
        existing_set = set()
        for user in existing:
            existing_set.add(user.username.lower())
        if user_name not in existing_set:
            serializer = UsernameSuggestionSerializer(
                data={"success": True}
            )
            serializer.is_valid(raise_exception=True)
            response = Response(serializer.data, status=status.HTTP_200_OK)
        else:
            suggested_names = get_similer_username(user_name, existing_set)
            serializer = UsernameSuggestionSerializer(
                data={
                        "success": False,
                        "message": "username already exist. please pick different username.",
                        "suggested_names": suggested_names
                    }
            )
            serializer.is_valid(raise_exception=True)
            response = Response(serializer.data, status=status.HTTP_200_OK)
        return response

        
