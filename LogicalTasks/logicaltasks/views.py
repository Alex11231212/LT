from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import Task


def index_view(request):
    num_tasks = Task.objects.count()
    return render(request, 'logicaltasks/index.html', context={'num_tasks':num_tasks})


class TaskListView(generic.ListView):

    def get_queryset(self):
        level = self.kwargs['level']
        return Task.objects.filter(difficulty__iexact=level)


class TaskDetailView(generic.DetailView):
    model = Task

    tasks = Task.objects.select_related('author', 'image', 'image_answer')\
            .prefetch_related('comment_set')

    def get_object(self, queryset=tasks):
        return queryset.get(slug__iexact=self.kwargs['task_slug'])
