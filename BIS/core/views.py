# core/views.py
import os
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.decorators import login_required

from .models import User, Role
#-----------------------------
#------startUser login--------
#-----------------------------
@csrf_exempt
def login(request):
    return render(request, 'login.html')

@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    print('Inside')
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse(status=403)

    email = user_data['email']
    first_name = user_data.get('given_name', '')
    last_name = user_data.get('family_name', '')

    user, created = User.objects.get_or_create(email=email)
    if created:
        ## Set user details
        user.first_name = first_name
        user.last_name = last_name
        ## Set default Role
        default_role, _ = Role.objects.get_or_create(name='CPDMO Staff')
        user.role = default_role
        user.save()
    
    auth_login(request, user)

    if user.role == "System Administrator":
        return redirect('sysadmin')
    else:
        return redirect('home')

@login_required()
def home(request):
    users = User.objects.all()
    user_data = request.session.get('user_data')
    return render(request, 'home.html', {'user_data': user_data, 'users' : users})

@login_required()
def sign_out(request):
    request.session.flush()
    return redirect('login')
#-----------------------------
#--------endUser login--------
#-----------------------------

#-----------------------------
#------startAdmin views-------
#-----------------------------
def sysadmin(request):
    return render(request, 'admin.html')
#-----------------------------
#--------endAdmin views-------
#-----------------------------
