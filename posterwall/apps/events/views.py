from django.shortcuts import render
from .models import Event

# Create your views here.
def events_view(request):
    events = Event.objects.all()
    return render(request, 'events/events-list.html', {
        'events': events,
    })
