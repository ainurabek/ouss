import datetime
from rest_framework.views import APIView
from ..opu.circuits.models import Circuit
from ..opu.objects.models import Object

now = datetime.datetime.now()
from django.views.generic import View

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.urls import reverse_lazy
from .forms import EventForm
from .models import Event, TypeOfJournal, Index, Choice
from django.http import HttpResponse, HttpResponseRedirect

class JournalList(ListView):
    """Список заявок"""
    model = TypeOfJournal
    template_name = 'dispatching/types_journals.html'
    context_object_name = 'types_journals'

    def get_context_data(self, *, pk=None, **kwargs):
        types_journal = TypeOfJournal.objects.all()
        context = {'types_journal': types_journal}
        return super().get_context_data(**context)


def event_list(request, journal_pk):
    journal = get_object_or_404(TypeOfJournal, pk=journal_pk)
    events = Event.objects.filter(type_journal=journal)
    choices = Choice.objects.all()
    return render(request, 'dispatching/event_list.html', {
        'events': events, 'choices': choices, 'journal': journal
    })


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'dispatching/event_detail.html', {
        'event': event
    })
class EventCreateView(View):
    """Создания отключения"""
    def post(self, request, pk):

        choice = Choice.objects.get(pk=pk)
        print(choice)
        form = EventForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.created_by = self.request.user.profile
            print(form.created_by)
            form.choice = choice
            form.save()
            return redirect('apps:dispatching:event_list')

    def get(self, request, pk):
        choice = Choice.objects.get(pk=pk)
        form = EventForm()
        return render(request, 'dispatching/request_create.html', {'form': form,
                                                                   'choice': choice
                                                                   })

def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            request1 = form.save(commit=False)
            request1.created_by = request.user.profile
            request1.created_at = datetime.datetime.now()
            request1.save()
            return redirect('apps:dispatching:event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'dispatching/request_create.html', {'form': form})


def event_delete(request, pk):
    Event.objects.get(pk=pk).delete()
    return redirect('apps:dispatching:event_list')


