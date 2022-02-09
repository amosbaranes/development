#-*- coding: utf-8 -*-
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Choice, Poll, ToDoForSamuel


def samuel(request):
    print(ToDoForSamuel.objects.all())
    return render(request, 'polls/samuel.html', {})


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        return Poll.objects.all()


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'


def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))


def vote_all(request):
    print(request.POST)
    for key, value in request.POST.items():
        if key == 'csrfmiddlewaretoken':
            continue
        # {'question-1': '2'}
        poll_id = key.split('-')[1]
        p = get_object_or_404(Poll, pk=poll_id)
        selected_choice = p.choice_set.get(pk=request.POST.get(key))
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results_all'))


class ResultsAll(generic.ListView):
    template_name = 'polls/results_all.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        return Poll.objects.all()