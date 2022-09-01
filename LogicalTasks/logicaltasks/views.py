from django.shortcuts import render

# Create your views here.
from django.views import generic


def index_view(request):

    return render(request, 'logicaltasks/base_template.html', context={})


class TaskList(generic.ListView):
    pass


class TaskDetail(generic.DetailView):
    pass