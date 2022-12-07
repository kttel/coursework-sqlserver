from django.shortcuts import get_object_or_404

from app import models
from . import forms


def set_book_edit_context(context, **kwargs):
    context['book'] = models.Book.objects.get(pk=kwargs.get('pk'))
    context['title'] = 'Editing book'
    context['action'] = 'Edit'
    genres_sql = "SELECT id, denomination from genre WHERE id NOT IN (SELECT g.id FROM genre g " \
                f"LEFT JOIN book_genre bg ON bg.genre_id = g.id WHERE bg.book_id = {kwargs.get('pk')})"
    context['genres'] = models.Tag.objects.raw(genres_sql)
    own_genres_sql = "SELECT id, denomination from genre WHERE id IN (SELECT g.id FROM genre g " \
                    f"LEFT JOIN book_genre bg ON bg.genre_id = g.id WHERE bg.book_id = {kwargs.get('pk')})"
    context['own_genres'] = models.Tag.objects.raw(own_genres_sql)
    authors_sql = "SELECT id, CONCAT(first_name, ' ', second_name) as fullname FROM author WHERE id NOT IN " \
                    "(SELECT a.id FROM author a LEFT JOIN book_author ba ON ba.author_id = a.id WHERE " \
                    f"ba.book_id = {kwargs.get('pk')})"
    context['authors'] = models.Author.objects.raw(authors_sql)
    own_authors_sql = "SELECT id, CONCAT(first_name, ' ', second_name) as fullname FROM author WHERE id IN " \
                        "(SELECT a.id FROM author a LEFT JOIN book_author ba ON ba.author_id = a.id WHERE " \
                        f"ba.book_id = {kwargs.get('pk')})"
    context['own_authors'] = models.Author.objects.raw(own_authors_sql)
    context['main_form'] = forms.BookForm(instance=context['book'])


def set_book_page_context(context, request, **kwargs):
    profile = models.Profile.objects.get(user=request.user)
    context['title'] = get_object_or_404(models.Book, pk=kwargs.get('pk')).title
    sql_authors = "SELECT a.id, CONCAT(first_name, ' ', second_name) as fullname, country, " \
                    "biography, birth_date, gender FROM author a INNER JOIN book_author ba ON " \
                f"ba.author_id = a.id WHERE ba.book_id = {kwargs.get('pk')}"
    context['authors'] = models.Author.objects.raw(sql_authors)
    context['reviews'] = models.Review.objects.filter(book_id=kwargs.get('pk'), moderated=1).order_by('-date_published')[:3]
    context['allowed_to_post'] = not models.Review.objects.filter(book_id=kwargs.get('pk'), profile=profile).exists()
    sql = f"SELECT g.id, g.denomination FROM genre g INNER JOIN book_genre bg ON bg.genre_id = g.id WHERE bg.book_id = {kwargs['pk']}"
    context['genres'] = models.Tag.objects.raw(sql)
    context['main_form'] = forms.ReviewForm()


def leave_review(request, **kwargs):
    title = request.POST.get('title')
    content = request.POST.get('content')
    vote = request.POST.get('vote')

    book = models.Book.objects.get(pk=kwargs.get('pk'))
    profile = models.Profile.objects.get(user=request.user)

    if vote:
        models.Review.objects.create(
            book=book,
            profile=profile,
            title=title,
            content=content,
            vote=vote
        )
    else:
        models.Review.objects.create(
            book=book,
            profile=profile,
            title=title,
            content=content
        )
