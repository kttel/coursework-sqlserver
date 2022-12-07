from django.urls import path

from . import views


urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('add_email/', views.EmailAdding.as_view(), name='add_email'),

    path('management/', views.ManagementPanelView.as_view(), name='management_panel'),

    path('management/add_tag/', views.CreateTagView.as_view(), name='add-tag'),
    path('management/add_genre/', views.CreateGenreView.as_view(), name='add-genre'),
    path('management/delete_tag/<int:pk>/', views.DeleteTagView.as_view(), name='delete-tag-admin'),
    path('management/delete_genre/<int:pk>/', views.DeleteGenreView.as_view(), name='delete-genre-admin'),

    path('management/author/add/', views.CreateAuthorView.as_view(), name='create-author'),
    path('management/author/add/result/', views.CreateAuthor.as_view(), name='create-author-result'),
    path('management/author/delete/<int:pk>/', views.DeleteAuthorView.as_view(), name='delete-author-data'),
    path('management/author/edit/<int:pk>/', views.EditAuthorView.as_view(), name='edit-author'),
    path('management/author/edit/<int:pk>/result/', views.EditAuthor.as_view(), name='edit-author-result'),

    path('management/add_publisher/', views.CreatePublisherView.as_view(), name='add-publisher'),
    path('management/delete_publisher/<int:pk>/', views.DeletePublisherView.as_view(), name='delete-publisher-admin'),
    path('management/get_publisher_books_amount/', views.GetPublisherBooksAmount.as_view(), name='get-publisher-books'),

    path('management/review/delete/<int:pk>/', views.DeleteUnconfirmedReview.as_view(), name='delete-unconfirmed-review'),
    path('management/review/confirm/<int:pk>/', views.ConfirmReview.as_view(), name='confirm-review'),
    path('management/reviews/confirm/', views.ConfirmAllReviews.as_view(), name='confirm-all'),

    path('management/log/', views.GetLastLog.as_view(), name='get-last-log'),

    path('edit/', views.ProfileEditingView.as_view(), name='edit-profile'),
]