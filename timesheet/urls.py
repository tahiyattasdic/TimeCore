# timesheet/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('clock-in/', views.clock_in, name='clock_in'),
    path('clock-out/', views.clock_out, name='clock_out'),
    path('signup/', views.sign_up, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # ADD THIS NEW LINE
    path('toggle_confirmation/<int:punch_id>/', views.toggle_confirmation, name='toggle_confirmation'),
]