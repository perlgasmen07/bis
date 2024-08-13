# core/views.py
import os
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.apps import apps
from .forms import UserForms
from django.db.models import F

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

    #-----------------------------
    #------Generic Model view-------
    #-----------------------------

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
        
        fields = []
        data = []

        if model_name == 'user':
            fields = ['id', 'first_name']
            data = list(model.objects.values(*fields))
        elif model_name == 'college':
            fields = ['id', 'shortname', 'description']
            data = list(model.objects.values(*fields))
        elif model_name == 'building':
            try:
                fields = ['id', 'shortname', 'college_shortname', 'inserted_by']
                data = list(model.objects.annotate(college_shortname=F('college__shortname')).values(*fields))
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        elif model_name == 'floor':
            fields = ['id', 'level']
            data = list(model.objects.values(*fields))
        elif model_name == 'room':
            fields = ['id', 'room_no']
            data = list(model.objects.values(*fields))
        elif model_name == 'attribute':
            fields = ['id', 'shortname']
            data = list(model.objects.values(*fields))
        elif model_name == 'property':
            fields = ['id', 'data']
            data = list(model.objects.values(*fields))

        return JsonResponse({'fields': fields, 'data': data}, safe=False)
    else:
        return JsonResponse({'error': 'Invalid model name'}, status=400)
    
    #-----------------------------
    #------One Data Views-------
    #-----------------------------
def get_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user_data = {
            'id': user.id,
            'first_name': user.first_name,
        }
        return JsonResponse(user_data, safe=False)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

def add_user(request):
    addUsersForm = UserForms

    if request.method == "POST":
        form = UserForms(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('sysadmin'))
        else:
            return render(request, 'user/addUser.html', {'addUsersForm':form, 'errors':form.errors})
    return render(request, 'user/addUser.html', {'addUsersForm':addUsersForm})

def edit_user(request, user_id):
    user = User.objects.get(user_id)
    return render(request)
#-----------------------------
#--------endAdmin views-------
#-----------------------------
