from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views import generic, View
from .models import Task
from django.http import HttpResponseRedirect

def index_view(request):
    num_tasks = Task.objects.count()
    return render(request, 'logicaltasks/index.html', context={'num_tasks':num_tasks})


class TaskListView(generic.ListView):

    def get_queryset(self):
        level = self.kwargs['level']
        return Task.objects.filter(difficulty=level)


class TaskDetailView(generic.DetailView):
    model = Task

    tasks = Task.objects.select_related('author', 'image', 'image_answer')\
            .prefetch_related('comment_set')

    def get_object(self, queryset=tasks):
        return queryset.get(slug=self.kwargs['task_slug'])


def reaction_view(request, reaction_on_task_or_comment):
    if reaction_on_task_or_comment in ['task_like', 'task_dislike']:
        task = get_object_or_404(Task, slug=request.POST.get('slug'))
        task.likes += 1
        task.save()
        return HttpResponseRedirect(task.get_task_url())


class Reaction(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = request.user
        options = {
            'task': self.task_reaction,
            'comment': self.comment_reaction,
            'article': self.article_reaction,
        }
        for k, v in options.items():
            if request.POST.get(k) is not None:
                return options[k](user=user, reaction=request.POST.get(k), pk=pk)

    def task_reaction(self, user, reaction, pk):
        is_liked = False
        is_disliked = False

        task = Task.objects.prefetch_related('likes', 'dislikes').get(pk=pk)
        if reaction == 'like':
            for u in task.dislikes.all():
                if u == user:
                    is_disliked = True
                    break
            if is_disliked:
                task.dislikes.remove(user)

            for u in task.likes.all():
                if u == user:
                    is_liked = True
                    break
            if not is_liked:
                task.likes.add(user)
            if is_liked:
                task.likes.remove(user)

        elif reaction == 'dislike':
            for u in task.likes.all():
                if u == user:
                    is_liked = True
                    break
            if is_liked:
                task.likes.remove(user)

            for u in task.dislikes.all():
                if u == user:
                    is_disliked = True
                    break
            if not is_disliked:
                task.dislikes.add(user)
            if is_disliked:
                task.dislikes.remove(user)

        return HttpResponseRedirect(task.get_task_url())


    def comment_reaction(self, ):
        pass

    def article_reaction(self, ):
        pass