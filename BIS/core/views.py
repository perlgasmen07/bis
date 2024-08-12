# core/views.py
import os
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.apps import apps

from .models import User, Role
from colleges.models import College
from buildings.models import Building
from floors.models import Floor, Room
from attributes.models import Attribute, Property, AttributeHistory, BuildingAttribute, PropertyHistory
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
    sysadmin_role =get_object_or_404(Role, name="System Administrator")
    if user.role == sysadmin_role:
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


def get_model(request, model_name):
    MODEL_MAP = {
        'user': 'core.User',
        'college': 'colleges.College',
        'building': 'buildings.Building',
        'floor': 'floors.Floor',
        'room': 'floors.Room',
        'attribute': 'attributes.Attribute',
        'property': 'attributes.Property',
    }

    if model_name in MODEL_MAP:
        model = apps.get_model(MODEL_MAP[model_name])
        
        # Customize the fields returned based on the model
        if model_name == 'user':
            data = model.objects.all().values('id', 'first_name')
            for item in data:
                item['shortname'] = item.pop('first_name')
        # elif model_name == 'attributes':
        #    data = model.objects.annotate(building_value=F('buildingattribute__value')).values('id', 'building_value')
        elif model_name == 'property':
            data = model.objects.all().values('id', 'data')
            for item in data:
                if isinstance(item['data'], dict):
                    # Extract the key name (e.g., 'longitude') instead of its value
                    # keys = item['data'].keys()
                    key_value_pair = [f"{key}: {value}" for key, value in item['data'].items()]
                    item['shortname'] = ', '.join(key_value_pair) if key_value_pair else 'N/A'
                else:
                    item['shortname'] = 'N/A'
        elif model_name == 'floor':
            data = model.objects.all().values('id', 'level')
            for item in data:
                item['shortname'] = item.pop('level')
        elif model_name == 'room':
            data = model.objects.all().values('id', 'room_no')
            for item in data:
                item['shortname'] = item.pop('room_no')
        else:
            data = model.objects.all().values('id', 'shortname')

        return JsonResponse(list(data), safe=False)

    else:
        return JsonResponse({'error': 'Invalid model name'}, status=400)

# def get_users(request):
#     users = User.objects.all().values('id','shortname')
#     return JsonResponse(list(users), safe=False)

# def get_user(request,user_id):
#     user = User.objects.get(user_id)

#     return JsonResponse(user, safe=False)

# def get_colleges(request):
#     colleges = College.objects.all().values('id', 'shortname')

#     return JsonResponse(list(colleges), safe=False)

# def get_college(request,college_id):
#     college = User.objects.get(college_id)

#     return JsonResponse(college, safe=False)

# def get_buildings(request):
#     buildings = Building.objects.all().values('id', 'shortname')

#     return JsonResponse(list(buildings), safe=False)

# def get_building(request, building_id):


def edit_user(request, user_id):
    user = User.objects.get(user_id)
    return render(request)
#-----------------------------
#--------endAdmin views-------
#-----------------------------
