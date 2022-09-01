from django.urls import path, re_path
from django.shortcuts import render, get_list_or_404
from . import views


app_name = 'logicaltasks'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('tasks/<str:level>/', views.TaskList.as_view(), name='task_list'),
    path('tasks/<slug:task>/', views.TaskDetail.as_view(), name='task_detail'),

    ]