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
    path('api/buildings/<int:college_id>/', building_views.get_buildings, name='get_buildings'),

    #view paths
    path('api/user/<int:user_id>', views.get_user, name='get_user'),
    path('api/college/<int:college_id>', college_views.get_college, name='get_college'),
    path('api/building/<int:building_id>', building_views.get_building, name='get_building'),
    path('api/attribute/<int:attribute_id>', attribute_views.get_attribute, name='get_attribute'),
    path('api/property/<int:property_id>', attribute_views.get_property, name='get_property'),
    path('api/floor/<int:floor_id>', floor_views.get_floor, name='get_floor'),
    path('api/room/<int:room_id>', floor_views.get_room, name='get_room'),

    #add paths
    path('api/user/n/', views.add_user, name='add_user'),
    path('api/college/n/', college_views.add_college, name='add_college'),
    path('api/building/n/', building_views.add_building, name='add_building'),
    path('api/attribute/n/', attribute_views.add_attribute, name='add_attribute'),
    path('api/property/n/', attribute_views.add_property, name='add_property'),
    path('api/floor/n/', floor_views.add_floor, name='add_floor'),
    path('api/room/n/', floor_views.add_room, name='add_room'),

    #edit paths
    path('api/user/<int:user_id>/e/', views.edit_user, name='edit_user'),
    path('api/college/<int:college_id>/e/', college_views.edit_college, name='edit_college'),
    path('api/building/<int:building_id>/e/', building_views.edit_building, name='edit_building'),
    path('api/attribute/<int:attribute_id>/e/', attribute_views.edit_attribute, name='edit_attribute'),
    path('api/property/<int:property_id>/e/', attribute_views.edit_property, name='edit_property'),
    path('api/floor/<int:floor_id>/e/', floor_views.edit_floor, name='edit_floor'),
    path('api/room/<int:room_id>/e/', floor_views.edit_room, name='edit_room'),

    #update path for data entry of CPDMO
    path('building/update/<int:building_id>/', building_views.update_building_view, name='update_building'),

    #detail
    path('building/<int:building_id>/', building_views.building_detail, name='building_detail'),

    #report
    path('report/', building_views.generate_building_report, name='generate_building_report'),
    path('export/building_report/csv/', building_views.export_building_report_csv, name='export_building_report_csv'),
    path('export/building_report/excel/', building_views.export_building_report_excel, name='export_building_report_excel'),

    #delete path
    path('api/user/<int:user_id>/d/', views.delete_user, name='delete_user'),
    path('api/college/<int:college_id>/d/', college_views.delete_college, name='delete_college'),
    path('api/building/<int:building_id>/d/', building_views.delete_building, name='delete_building'),
    path('api/attribute/<int:attribute_id>/d/', attribute_views.delete_attribute, name='delete_attribute'),
    path('api/property/<int:property_id>/d/', attribute_views.delete_property, name='delete_property'),
    path('api/floor/<int:floor_id>/d/', floor_views.delete_floor, name='delete_floor'),
    path('api/room/<int:room_id>/d/', floor_views.delete_room, name='delete_room'),

    #recover path
    path('api/user/<int:user_id>/r/', views.recover_user, name='recover_user'),
    path('api/college/<int:college_id>/r/', college_views.recover_college, name='recover_college'),
    path('api/building/<int:building_id>/r/', building_views.recover_building, name='recover_building'),
    path('api/attribute/<int:attribute_id>/r/', attribute_views.recover_attribute, name='recover_ttribute'),
    path('api/property/<int:property_id>/r/', attribute_views.recover_property, name='recover_property'),
    path('api/floor/<int:floor_id>/r/', floor_views.recover_floor, name='recover_floor'),
    path('api/room/<int:room_id>/r/', floor_views.recover_room, name='recover_room'),

]

