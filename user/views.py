from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import (UserSerializer, AuthTokenSerializer,)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@csrf_exempt
def login_view(request):
   return render(request,'user/login.html')

def register_page(request):
    return render(request, 'user/register.html')

@login_required(login_url='/user/login/')
def dashboard_page(request):
   return render(request,'user/dashboard.html')

@login_required(login_url='/user/login/')
def transactions_page(request):
   return render(request,'user/transactions.html')

class CreateUserView(generics.CreateAPIView):
  serializer_class=UserSerializer

@method_decorator(csrf_exempt, name='dispatch')
class CreateTokenView(ObtainAuthToken):
  serializer_class=AuthTokenSerializer
  renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
  serializer_class=UserSerializer
  authentication_classes=[authentication.TokenAuthentication]
  permission_classes=[permissions.IsAuthenticated]

  def get_object(self):
    return self.request.user

