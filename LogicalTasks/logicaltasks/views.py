import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.forms import ModelForm
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views import generic, View

from .forms import CommentForm
from .models import Task, LikeDislike, Comment
from django.http import HttpResponseRedirect, HttpResponse


def index_view(request):
    num_tasks = Task.objects.count()
    return render(request, 'logicaltasks/index.html', context={'num_tasks':num_tasks})


class TaskListView(generic.ListView):
    def get_queryset(self):
        level = self.kwargs['level']
        return Task.objects.filter(difficulty=level)

@login_required
def task_detail_view(request, task_slug):
    template = 'logicaltasks/task_detail.html'
    tasks = Task.objects.select_related('author', 'image', 'image_answer') \
        .prefetch_related('comment_set')
    task = get_object_or_404(tasks, slug=task_slug)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            text = comment_form.cleaned_data['text']
            new_comment = Comment.objects.create(
                task=task,
                author=request.user,
                text=text,
            )
            new_comment.save()
            return HttpResponseRedirect(request.path_info)
    elif request.method == 'GET':
        comment_form = CommentForm()

    return render(request, template, context={
        'task': task,
        'form': comment_form,
    })


class ReactionView(LoginRequiredMixin, View):
    model = None  # Data Model - Articles or Comments
    vote_type = None  # Vote type Like/Dislike

    def post(self, request, pk, **kwargs):
        obj = self.model.objects.get(pk=pk)
        # GenericForeignKey does not support get_or_create
        try:
            likedislike = LikeDislike.objects.get(
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.id, user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.reaction.create(user=request.user, vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.reaction.likes().count(),
                "dislike_count": obj.reaction.dislikes().count(),
                "sum_rating": obj.reaction.sum_rating()
            }),
            content_type="application/json"
        )


