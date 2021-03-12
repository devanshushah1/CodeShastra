from django.shortcuts import render

# Create your views here.

from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from .models import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
# Create your views here.
# f_url = 'http//localhost:3000'
# def EmailVerification(User):
    

class RegisterView(APIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        # username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("emailid")
        firstname = request.data.get("firstname")
        phonenumber = request.data.get("phonenumber")
        state = request.data.get("state")
        district = request.data.get("district")
        if request.user:
            if password is None or email is None or firstname is None or phonenumber is None or state is None or district is None:
                return Response({'error': 'Please provide all the user information'},
                                status=status.HTTP_400_BAD_REQUEST)
            user = CustomUser.objects.create_user(email=email, password=password)
            user.save()
            if not user:
                return Response({'error': 'User not created'},
                                status=status.HTTP_404_NOT_FOUND)
            user.email = email
            user.first_name = firstname
            user.phone_number= phonenumber
            user.state=state
            user.district=district
            user.save()
            user_data = {
                'msg': 'User created successfuly',
                'user': {
                    'userid': user.id,
                    # 'username': user.username,
                    'emailid': user.email,
                    'firstname': user.first_name,
                    'phonenumber': user.phone_number,
                    'state': user.state,
                    'district': user.district
                }
            }
            return Response(user_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not authorized'},
                            status=status.HTTP_400_BAD_REQUEST)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        token = get_tokens_for_user(user)
        user_data = {
            'token': token,
            'user': {
                'userid': user.id,
                'username': user.username,
                'emailid': user.email,
            }
        }
        return Response(user_data, status=status.HTTP_200_OK)
