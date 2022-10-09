from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.shortcuts import render, get_list_or_404
from . import views
from .models import Task, LikeDislike, Comment


app_name = 'logicaltasks'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('tasks/<level>/', views.TaskListView.as_view(), name='task_list'),
    path('task/<slug:task_slug>/', views.task_detail_view, name='task_detail'),
    path('task/<int:pk>/like/',
         views.ReactionView.as_view(model=Task, vote_type=LikeDislike.LIKE),
         name='task_like'),
    path('task/<int:pk>/dislike/',
         views.ReactionView.as_view(model=Task, vote_type=LikeDislike.DISLIKE),
         name='task_dislike'),
    path('comment/<int:pk>/like/',
         views.ReactionView.as_view(model=Comment, vote_type=LikeDislike.LIKE),
         name='comment_like'),
    path('comment/<int:pk>/dislike/',
         views.ReactionView.as_view(model=Comment, vote_type=LikeDislike.DISLIKE),
         name='comment_dislike')

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)