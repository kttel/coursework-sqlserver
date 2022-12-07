from django.urls import path

from . import views


urlpatterns = [
    path('', views.BooksListView.as_view(), name='books'),
    path('book/<int:pk>/', views.SingleBookView.as_view(), name='book'),
    path('book/add/', views.BookCreationView.as_view(), name='add-book'),
    path('book/add/result/', views.BookCreation.as_view(), name='add-book-result'),
    path('book/edit/<int:pk>/', views.BookEditingView.as_view(), name='edit-book'),
    path('book/edit/<int:pk>/result/', views.BookEditing.as_view(), name='edit-book-result'),
    path('book/edit/<int:pk>/genre-create/', views.GenreAddingToBook.as_view(), name='add-genre'),
    path('book/edit/<int:pk>/genre-delete/', views.GenreDeleteFromBook.as_view(), name='delete-genre-from-book'),
    path('book/delete/<int:pk>/', views.BookDeleteView.as_view(), name='book-delete'),
    path('book/edit/<int:pk>/author-add/', views.AuthorAddingToBook.as_view(), name='add-author-to-book'),
    path('book/edit/<int:pk>/author-delete/', views.AuthorDeleteFromBook.as_view(), name='delete-author-from-book'),
    path('book/review/delete/<int:pk>/', views.DeleteReviewView.as_view(), name='delete-review'),
]