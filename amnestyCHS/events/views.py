from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Event
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .forms import EventForm
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.core.paginator import EmptyPage, PageNotAnInteger
# Create your views here.
 
  
def staff_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect_to_login(request.get_full_path(), login_url='/admin/login/')
        if not user.is_staff:
            raise PermissionDenied("Access denied. You must be a staff member to view this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@staff_required
def event_create_view(request):
    if request.method =='POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()

    return render(request, 'events/event_form.html', {'form': form})  # renders the form for creating events and passes context to the template

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'event_list'
    paginate_by = 5
    ordering_by = ['-date']  # responsible for pagination and ordering of the events

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except(EmptyPage, PageNotAnInteger):
            return redirect('event_list')
    
class EventDetailView(DetailView): 
    model  = Event 
    template_name = 'events/event_detail.html'  # shows an individual event and its details as well as 2 related events
    context_object_name  = 'event_item' 
                                                                                                        