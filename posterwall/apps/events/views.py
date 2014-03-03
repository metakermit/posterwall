from django.shortcuts import render

# Create your views here.
def events_view(request):
    return render(request, 'events/events-list.html')
