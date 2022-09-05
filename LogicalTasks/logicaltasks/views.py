from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import Task


def index_view(request):

    return render(request, 'logicaltasks/base_template.html', context={})


class TaskListView(generic.ListView):
    def get_queryset(self):
        levels_map = {
            'easy': 'e',
            'medium': 'm',
            'hard': 'h',
        }
        level = self.kwargs['level']
        return Task.objects.filter(difficulty__iexact=levels_map.get(level))


class TaskDetailView(generic.DetailView):
    pass