from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from .forms import EventForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .permissions import event_manager_permission


def event_list(request):

    query = request.GET.get('search_item')

    if query:
        events = Event.objects.filter(Q(title__icontains=query) | Q(location__icontains=query))
    else:
        events = Event.objects.all()


    return render(request, 'events/event_list.html', {'events': events})

@login_required(login_url='login')
@event_manager_permission
def add_event(request):

    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            event = form.save()

            return redirect('event_list')
    else:
        form = EventForm()

        return render(request, 'events/add_event.html', {'form': form})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)

    return render(request, 'events/event_detail.html', {'event': event})