from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, EventTicket, EventImage
from .forms import EventForm, EventImageFormSet
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .permissions import event_manager_permission, delete_event_permission, change_event_permission
import logging
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import View, ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy

logger = logging.getLogger(__name__)


class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 8


    def get_queryset(self):
        # queryset = super().get_queryset()

        title = self.request.GET.get('title')
        location = self.request.GET.get('location')

        filters = Q()

        if title and location:
            filters &= Q(title__icontains=title) & Q(location__icontains=location)
        elif title:
            filters |= Q(title__icontains=title)
        elif location:
            filters |= Q(location__icontains=location)

        if title or location:
            events = self.model.objects.filter(filters)
        else:
            events = self.model.objects.all()

        return events

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['test'] = 'Satesto Saxeli'

        return context



# class EventListView(View):
#
#     @staticmethod
#     def get(request):
#         title = request.GET.get('title')
#         location = request.GET.get('location')
#
#         # logger.warning(f'Filtering: Title - {title}, Location - {location}')
#
#         filters = Q()
#
#         # if query:
#         #     events = Event.objects.filter(Q(title__icontains=query) | Q(location__icontains=query))
#         # else:
#         #     events = Event.objects.all()
#
#         if title and location:
#             filters &= Q(title__icontains=title) & Q(location__icontains=location)
#         elif title:
#             filters |= Q(title__icontains=title)
#         elif location:
#             filters |= Q(location__icontains=location)
#
#         if title or location:
#             events = Event.objects.filter(filters)
#         else:
#             events = Event.objects.all()
#
#         paginator = Paginator(events, 8)
#
#         try:
#             page = request.GET.get('page')
#             events = paginator.page(page)
#         except PageNotAnInteger:
#             events = paginator.page(1)
#         except EmptyPage:
#             events = paginator.page(paginator.num_pages)

        # logger.info(f'Event Count: {events.count()}')

        # return render(request, 'events/event_list.html', {'events': events})

#
# def event_list(request):
#
#     # logger.info('Started Index Page Logic')
#
#     title = request.GET.get('title')
#     location = request.GET.get('location')
#
#     # logger.warning(f'Filtering: Title - {title}, Location - {location}')
#
#     filters = Q()
#
#     # if query:
#     #     events = Event.objects.filter(Q(title__icontains=query) | Q(location__icontains=query))
#     # else:
#     #     events = Event.objects.all()
#
#     if title and location:
#         filters &= Q(title__icontains=title) & Q(location__icontains=location)
#     elif title:
#         filters |= Q(title__icontains=title)
#     elif location:
#         filters |= Q(location__icontains=location)
#
#
#     if title or location:
#         events = Event.objects.filter(filters)
#     else:
#         events = Event.objects.all()
#
#
#     paginator = Paginator(events, 8)
#
#     try:
#         page = request.GET.get('page')
#         events = paginator.page(page)
#     except PageNotAnInteger:
#         events = paginator.page(1)
#     except EmptyPage:
#         events = paginator.page(paginator.num_pages)
#
#
#     # logger.info(f'Event Count: {events.count()}')
#
#     return render(request, 'events/event_list.html', {'events': events})

# @login_required(login_url='login')
# @event_manager_permission
# def add_event(request):
#
#     if request.method == 'POST':
#         image_formset = EventImageFormSet(request.POST, files=request.FILES)
#         event_form = EventForm(request.POST)
#
#         if event_form.is_valid() and image_formset.is_valid():
#             event = event_form.save()
#
#             for image_form in image_formset:
#                 if image_form.cleaned_data.get('image'):
#                     print("image", image_form.cleaned_data.get('image'))
#                     image = image_form.save(commit=False)
#                     image.event = event
#                     image.save()
#
#             return redirect('event_list')
#     else:
#         event_form = EventForm()
#         image_formset = EventImageFormSet()
#
#         return render(request, 'events/add_event.html', {'event_form': event_form, 'image_formset': image_formset})


class CreateEventView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/add_event.html'
    success_url = reverse_lazy('core:event_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['image_formset'] = EventImageFormSet(queryset=EventImage.objects.none())

        return context

    def form_valid(self, form):
        event = form.save()

        image_formset = EventImageFormSet(self.request.POST, files=self.request.FILES)

        for image_form in image_formset:
            if image_form.is_valid():
                image = image_form.save(commit=False)
                image.event = event
                image.save()

        return redirect(self.success_url)


    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

# def event_detail(request, pk):
#     event = get_object_or_404(Event, pk=pk)
#
#     return render(request, 'events/event_detail.html', {'event': event})

class EventDetailView(DetailView):
    model = Event
    context_object_name = 'event'
    template_name = 'events/event_detail.html'


def buy_ticket(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if event.sold_out():
        return HttpResponse('All Tickets Are Sold')

    event_ticket, created = EventTicket.objects.get_or_create(event=event, user=request.user)

    if created:
        event_ticket.ticket_count = 1
    else:
        event_ticket.ticket_count += 1

    event_ticket.save()

    event.ticket_count -= 1
    event.save()

    send_mail('Buy Ticket', f'{request.user.username} has successfully bought ticket on event: {event.title}', settings.DEFAULT_FROM_EMAIL, [request.user.email], fail_silently=False)

    return redirect('event_list')


# @login_required(login_url='login')
# @delete_event_permission
# def delete_event(request, pk):
#     event = get_object_or_404(Event, pk=pk)
#
#     # if request.method == 'POST':
#     event.delete()
#
#     return redirect('event_list')

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('core:event_list')


# @login_required(login_url='login')
# @change_event_permission
# def change_event(request, pk):
#     event = get_object_or_404(Event, pk=pk)
#     print(f'HTTP REFERER: {request.META.get('HTTP_REFERER')}')
#     if request.method == 'POST':
#         form = EventForm(request.POST, instance=event)
#
#         if form.is_valid():
#             event = form.save()
#
#             return redirect('event_detail', pk=pk)
#     else:
#         form = EventForm(instance=event)
#
#         return render(request, 'events/change_event.html', {'form': form})


class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/change_event.html'

    def get_success_url(self):
        success_url = reverse_lazy('core:event_detail', kwargs={'pk': self.object.pk})
        return success_url
