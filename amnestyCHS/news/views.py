from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import News
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .forms import NewsForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login
from django.db import IntegrityError
from django.core.paginator import EmptyPage, PageNotAnInteger


def staff_required(view_func):
    def _wrapped_view(request, *args, **kwargs): #helper function to check if the user is staff
        user = request.user
        if not user.is_authenticated:
            return redirect_to_login(request.get_full_path(), login_url='/admin/login/')
        if not user.is_staff:
            raise PermissionDenied("Access denied. You must be a staff member to view this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@staff_required
def news_create_view(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('news_list')  # try except to catch potential db or other errors
            except IntegrityError:
                form.add_error(None, "There was an error saving the news item. Please try again.")
            except Exception as e:
                form.add_error(None, f"An unexpected error occurred: {str(e)}")
    else:
        form = NewsForm()

    return render(request, 'news/news_form.html', {'form': form}) # renders the form for creating news and passes context to the template


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10                        # responsible for pagination and ordering of the newsa
    ordering = ['-published_date']

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs) # handles pagination and ordering errors if db is down
        except (EmptyPage, PageNotAnInteger):
           return redirect('news_list')
        

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'             # shows an individual news item and its details as well as 2 related news items 
    context_object_name = 'news_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_news'] = News.objects.exclude(id=self.object.id).order_by('-published_date')[:2]
        return context