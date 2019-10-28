from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.user_login, name="user_login"),
    path('logout/', views.user_logout, name="user_logout"),
    path('employeedashboard/', views.employeedashboard, name="employeedashboard"),
    path('managerdashboard/', views.managerdashboard, name="managerdashboard"),
    path('applyleave/', views.applyleave, name="applyleave"),
    path('approveleave/<leave_id>/', views.approveleave, name="approveleave"),
    path('rejectleave/<leave_id>/', views.rejectleave, name="rejectleave"),
    path('deleteleave/<leave_id>/', views.deleteleave, name="deleteleave"),
]