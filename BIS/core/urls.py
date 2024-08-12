from django.urls import path
from . import views
from colleges import views as college_views
from buildings import views as building_views
from attributes import views as attribute_views
from floors import views as floor_views

urlpatterns = [
    path('accounts/login/', views.login, name='login'),
    path('sign-out', views.sign_out, name='sign_out'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    path('home/', views.home, name='home'),
    path('sysadmin/', views.sysadmin, name="sysadmin"),
    path('api/<str:model_name>/', views.get_model, name='get_model'),
    # path('/api/users', views.get_users, name='users'),
    # path('/api/colleges', college_views.get_colleges, name='colleges'),
    # path('/api/buildings', building_views.get_buildings, name='buildings'),
    # path('/api/attributes', attribute_views.get_attributes, name='attributes'),
    # path('/api/properties', attribute_views.get_properties, name='properties'),
    # path('/api/floors', floor_views.get_floors, name='floors'),
    # path('/api/rooms', floor_views.get_rooms, name='rooms'),
]

