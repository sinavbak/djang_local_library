from django.shortcuts import render
from .models import Book,BookInstance,Genre,Author,Languange
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required    
def index(request):
    num_books = Book.objects.all().count()
    num_instance=BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()
    num_authors = Author.objects.count()
    num_genre = Genre.objects.count()
    num_book_search = Book.objects.filter(title__icontains = 'Ozan').count()
    num_languange = Languange.objects.count()
    
    # Set Session
    #del request.session['num_visits']
    num_visits = request.session.get('num_visits',1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_books': num_books,
        'num_instance':num_instance,
        'num_instance_available':num_instances_available,
        'num_authors':num_authors,
        'num_genre':num_genre,
        'num_book_search':num_book_search,
        'num_languange':num_languange,
        'num_visits':num_visits
    }
    return render(request, 'index.html', context = context)

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class BookListView(LoginRequiredMixin,generic.ListView):
    model = Book
    paginate_by = 1
    
class BookDetailView(generic.DetailView):
    model = Book
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 1
class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(browwer=self.request.user).filter(status__exact='o').order_by('due_back')
    

from django.contrib.auth.mixins import PermissionRequiredMixin
#@permission_required('can_view_all')
class AllBorrowedBooksListView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'catalog.can_view_all'
    model = BookInstance
    template_name ='catalog/all_borrowed_books.html'
    paginate_by = 10
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm
from django.contrib.auth.decorators import permission_required

@permission_required('catalog.can_view_all')
def renew_book_librarian(request,pk):

    book_instance = get_object_or_404(BookInstance,pk = pk)
    if request.method == "POST":
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today()+datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renawal_date':proposed_renewal_date})
    context = {
        'form' : form,
        'book_instance':book_instance,
    }
    return render(request,'catalog/book_renew_librarian.html',context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
class AuthorCreate(PermissionRequiredMixin,CreateView):
    permission_required = "catalog.can_do_stufs" 
    model = Author
    fields = '__all__'
    initial = {'date_of_death':'05/01/2018'}
class AuthorUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = "catalog.can_do_stufs"
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
class AuthorDelete(PermissionRequiredMixin,DeleteView):
    permission_required = "catalog.can_do_stufs"
    model = Author
    success_url = reverse_lazy('author')

# BOOK EDITING
class BookCreate(PermissionRequiredMixin,CreateView):
    permission_required ="catalog.can_do_stufs"
    model = Book
    fields = '__all__'
class BookUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'catalog.can_do_stufs'
    model = Book
    fields = '__all__'
class BookDelete(PermissionRequiredMixin,DeleteView):
    permission_required = 'catalog.can_do_stufs'
    model = Book
    success_url = reverse_lazy('books') 
    