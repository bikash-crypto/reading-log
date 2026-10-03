from django.contrib import messages
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import BookForm
from .models import Author, Book


class BookListView(ListView):
    """The shelf: every book as a spine, with a status filter and search."""
    model = Book
    template_name = 'library/book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        books = Book.objects.select_related('author')
        self.query = self.request.GET.get('q', '').strip()
        self.status = self.request.GET.get('status', '')
        if self.status in Book.Status.values:
            books = books.filter(status=self.status)
        if self.query:
            books = books.filter(
                Q(title__icontains=self.query) | Q(author__name__icontains=self.query)
            )
        return books

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        counts = dict(Book.objects.values_list('status').annotate(n=Count('id')))
        context['tabs'] = [('', 'All books', sum(counts.values()))] + [
            (value, label, counts.get(value, 0)) for value, label in Book.Status.choices
        ]
        context['query'] = self.query
        context['status'] = self.status
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'

    def get_queryset(self):
        return Book.objects.select_related('author').prefetch_related('genres')


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_form.html'

    def form_valid(self, form):
        messages.success(self.request, f'Added “{form.instance.title}” to your shelf.')
        return super().form_valid(form)


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Changes saved.')
        return super().form_valid(form)


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'library/book_confirm_delete.html'
    success_url = reverse_lazy('library:book_list')

    def form_valid(self, form):
        messages.success(self.request, f'Removed “{self.object.title}” from your shelf.')
        return super().form_valid(form)


class AuthorListView(ListView):
    model = Author
    template_name = 'library/author_list.html'
    context_object_name = 'authors'

    def get_queryset(self):
        return Author.objects.annotate(book_count=Count('books'))


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'library/author_detail.html'
