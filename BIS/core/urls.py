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
    
    #read path
    path('api/<str:model_name>/', views.get_model, name='get_model'),

    #view paths
    path('api/user/<int:user_id>', views.get_user, name='get_user'),
    path('api/college/<int:college_id>', college_views.get_college, name='get_college'),
    path('api/building/<int:building_id>', building_views.get_building, name='get_building'),
    path('api/attribute/<int:attribute_id>', attribute_views.get_attribute, name='get_attribute'),
    path('api/property/<int:property_id>', attribute_views.get_property, name='get_property'),
    path('api/floor/<int:floor_id>', floor_views.get_floor, name='get_floor'),
    path('api/room/<int:room_id>', floor_views.get_room, name='get_room'),

    #add paths
    #path('api/user/n/', views.add_user, name='add_user'),
    path('api/college/n/', college_views.add_college, name='add_college'),
    path('api/building/n/', building_views.add_building, name='add_building'),
    path('api/attribute/n/', attribute_views.add_attribute, name='add_attribute'),
    path('api/property/n/', attribute_views.add_property, name='add_property'),
    path('api/floor/n/', floor_views.add_floor, name='add_floor'),
    path('api/room/n/', floor_views.add_room, name='add_room'),

    #edit paths
    path('api/user/e/<int:user_id>', views.edit_user, name='edit_user')
    #delete path
]

