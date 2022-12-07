from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from app import models, mixins

from . import forms, business_logic


class BooksListView(ListView):
    paginate_by = 5
    template_name = 'books/books_list.html'
    model = models.Book
    context_object_name = 'books'

    def get_queryset(self):
        search = self.request.GET.get('search', '')
        author = self.request.GET.get('author', '')
        sql_append = f" ba.author_id = {author} AND " if author != '' else ''
        sql = "SELECT DISTINCT b.id, b.title, CAST(b.synopsis AS VARCHAR(MAX)) as synopsis, (SELECT TOP 1 CONCAT(a.first_name, ' ', a.second_name) FROM author a " \
              "LEFT JOIN book_author ba ON ba.book_id = b.id WHERE a.id = ba.author_id) AS b_author FROM book b " \
             f"LEFT JOIN book_author ba ON ba.book_id = b.id " \
             f"WHERE {sql_append} (b.title LIKE '%%{search}%%' OR b.synopsis LIKE '%%{search}%%')"
        books = models.Book.objects.raw(sql)
        return books

    def get_context_data(self, **kwargs):
        context = super(BooksListView, self).get_context_data(**kwargs)
        context['title'] = 'Book list'
        sql_authors = "SELECT id, first_name, second_name, country, biography, birth_date, gender FROM author"
        context['authors'] = models.Author.objects.raw(sql_authors)
        context['search'] = self.request.GET.get('search', '')
        context['author'] = self.request.GET.get('author', '')
        return context


class SingleBookView(DetailView):
    model = models.Book
    pk_url_kwarg = 'pk'
    context_object_name = 'book'
    template_name = 'books/book_details.html'

    def post(self, request, *args, **kwargs):
        business_logic.leave_review(self.request, **self.kwargs)
        messages.success(request, 'Review was added! Wait for confirmation by admin.')
        return redirect('book', pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super(SingleBookView, self).get_context_data(**kwargs)
        business_logic.set_book_page_context(context, self.request, **self.kwargs)
        return context


class BookCreationView(mixins.RedirectIfNotStuff, LoginRequiredMixin, TemplateView):
    template_name = 'books/edit_book.html'

    def get_context_data(self, **kwargs):
        context = super(BookCreationView, self).get_context_data(**kwargs)
        context['title'] = 'Adding book'
        context['action'] = 'Add'
        context['main_form'] = forms.BookForm()
        return context


class BookCreation(mixins.RedirectIfNotStuff, LoginRequiredMixin, CreateView):
    model = models.Book
    fields = ['title', 'isbn', 'synopsis', 'publisher', 'img']

    def form_valid(self, form):
        messages.success(self.request, 'You added new book!')
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def form_invalid(self, form):
        return redirect('add-book')

    def get_success_url(self):
        return reverse_lazy('book', kwargs={'pk': self.object.pk})


class BookEditingView(mixins.RedirectIfNotStuff, LoginRequiredMixin, TemplateView):
    template_name = 'books/edit_book.html'

    def get_context_data(self, **kwargs):
        context = super(BookEditingView, self).get_context_data(**kwargs)
        business_logic.set_book_edit_context(context, **self.kwargs)
        return context


class BookEditing(mixins.RedirectIfNotStuff, LoginRequiredMixin, UpdateView):
    model = models.Book
    fields = ['title', 'isbn', 'synopsis', 'publisher', 'img']

    def form_valid(self, form):
        messages.success(self.request, 'You updated this book!')
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def form_invalid(self, form):
        messages.error(self.request, 'Something went wrong!')
        return reverse_lazy('book', kwargs={'pk': self.kwargs.get('pk')})

    def get_success_url(self):
        return reverse_lazy('book', kwargs={'pk': self.kwargs.get('pk')})


class GenreAddingToBook(mixins.RedirectIfNotStuff, LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        book = models.Book.objects.get(pk=self.kwargs.get('pk'))
        genre = models.Genre.objects.get(pk=int(request.POST.get('genre')))

        models.BookGenre.objects.create(book=book, genre=genre)
        messages.success(self.request, f"You added new genre: { genre.denomination }!")
        return redirect('book', pk=self.kwargs.get('pk'))


class GenreDeleteFromBook(mixins.RedirectIfNotStuff, LoginRequiredMixin, DeleteView):
    def post(self, request, *args, **kwargs):
        book = models.Book.objects.get(pk=self.kwargs.get('pk'))
        genre = models.Genre.objects.get(pk=int(request.POST.get('genre')))

        book_genre = models.BookGenre.objects.filter(book=book, genre=genre)
        if book_genre.exists():
            book_genre[0].delete()
        messages.success(self.request, f"You deleted genre: { genre.denomination }!")
        return redirect('book', pk=self.kwargs.get('pk'))


class BookDeleteView(mixins.RedirectIfNotStuff, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'delete_template.html'
    model = models.Book
    success_message = "Book was deleted successfully!"
    success_url = reverse_lazy('books')
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(BookDeleteView, self).get_context_data(**kwargs)
        context['object'] = models.Book.objects.get(pk=self.kwargs.get('pk')).title
        context['type'] = 'books'
        context['title'] = 'Deleting'
        context.update(self.kwargs)
        return context


class AuthorAddingToBook(mixins.RedirectIfNotStuff, LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        book = models.Book.objects.get(pk=self.kwargs.get('pk'))
        author = models.Author.objects.get(pk=int(request.POST.get('author')))

        models.BookAuthor.objects.create(book=book, author=author)
        messages.success(self.request, f"You added new author to the book: {author.first_name} {author.second_name}")
        return redirect('book', pk=self.kwargs.get('pk'))


class AuthorDeleteFromBook(mixins.RedirectIfNotStuff, LoginRequiredMixin, DeleteView):
    def post(self, request, *args, **kwargs):
        book = models.Book.objects.get(pk=self.kwargs.get('pk'))
        author = models.Author.objects.get(pk=int(request.POST.get('author')))

        book_author = models.BookAuthor.objects.filter(book=book, author=author)
        if book_author.exists():
            book_author[0].delete()
        messages.success(self.request, f"You deleted author from this book: {author.first_name} {author.second_name}!")
        return redirect('book', pk=self.kwargs.get('pk'))


class DeleteReviewView(mixins.RedirectIfNotOwnReview, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = models.Review
    pk_url_kwarg = 'pk'
    template_name = 'delete_template.html'
    success_message = "Review was deleted successfully!"

    def post(self, request, *args, **kwargs):
        book = models.Review.objects.get(pk=self.kwargs.get('pk')).book
        self.kwargs.update({'book_id': book.pk})
        return super(DeleteReviewView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('book', kwargs={'pk': self.kwargs.get('book_id')})
