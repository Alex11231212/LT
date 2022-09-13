from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.shortcuts import render, get_list_or_404
from . import views


app_name = 'logicaltasks'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('tasks/<str:level>/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/<str:level>/<slug:task_slug>/', views.TaskDetailView.as_view(), name='task_detail'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)