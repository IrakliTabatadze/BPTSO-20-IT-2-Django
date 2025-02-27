from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from .forms import EventForm, EventImageFormSet
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .permissions import event_manager_permission, delete_event_permission, change_event_permission
import logging
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

logger = logging.getLogger(__name__)

def event_list(request):

    # logger.info('Started Index Page Logic')

    title = request.GET.get('title')
    location = request.GET.get('location')

    # logger.warning(f'Filtering: Title - {title}, Location - {location}')

    filters = Q()

    # if query:
    #     events = Event.objects.filter(Q(title__icontains=query) | Q(location__icontains=query))
    # else:
    #     events = Event.objects.all()

    if title and location:
        filters &= Q(title__icontains=title) & Q(location__icontains=location)
    elif title:
        filters |= Q(title__icontains=title)
    elif location:
        filters |= Q(location__icontains=location)


    if title or location:
        events = Event.objects.filter(filters)
    else:
        events = Event.objects.all()


    paginator = Paginator(events, 8)

    try:
        page = request.GET.get('page')
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)


    # logger.info(f'Event Count: {events.count()}')

    return render(request, 'events/event_list.html', {'events': events})

@login_required(login_url='login')
@event_manager_permission
def add_event(request):

    if request.method == 'POST':
        image_formset = EventImageFormSet(request.POST, files=request.FILES)
        event_form = EventForm(request.POST)

        if event_form.is_valid() and image_formset.is_valid():
            event = event_form.save()

            for image_form in image_formset:
                if image_form.cleaned_data.get('image'):
                    print("image", image_form.cleaned_data.get('image'))
                    image = image_form.save(commit=False)
                    image.event = event
                    image.save()

            return redirect('event_list')
    else:
        event_form = EventForm()
        image_formset = EventImageFormSet()

        return render(request, 'events/add_event.html', {'event_form': event_form, 'image_formset': image_formset})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)

    return render(request, 'events/event_detail.html', {'event': event})


@login_required(login_url='login')
@delete_event_permission
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    # if request.method == 'POST':
    event.delete()

    return redirect('event_list')

@login_required(login_url='login')
@change_event_permission
def change_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    print(f'HTTP REFERER: {request.META.get('HTTP_REFERER')}')
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)

        if form.is_valid():
            event = form.save()

            return redirect('event_detail', pk=pk)
    else:
        form = EventForm(instance=event)

        return render(request, 'events/change_event.html', {'form': form})
