from django.urls import path
from . import views

urlpatterns = [
    path('accounts/login/', views.login, name='login'),
    path('sign-out', views.sign_out, name='sign_out'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    path('home/', views.home, name='home'),
    path('admin/', views.sysadmin, name="admin"),
]

