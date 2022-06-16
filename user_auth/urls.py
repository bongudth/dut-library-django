from django.urls import path
from . import views

app_name = 'user_auth'

urlpatterns = [
    path('login/', views.login_account, name='login'),
    path('register/', views.register_account, name='register'),
    path('logout/', views.logout_account, name='logout'),
]
