from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.PostsListView.as_view(), name='posts'),
    path('post/<int:pk>/', views.SinglePostView.as_view(), name='post'),
    path('post/edit/<int:pk>/', views.PostEditView.as_view(), name='post-edit'),
    path('post/edit/<int:pk>/result/', views.PostEditing.as_view(), name='post-editing-result'),
    path('post/edit/<int:pk>/tag-create/', views.TagAddingToPost.as_view(), name='add-tag'),
    path('post/edit/<int:pk>/tag-delete/', views.TagDeleteFromPost.as_view(), name='delete-tag'),
    path('post/create/', views.PostCreationView.as_view(), name='post-create'),
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view(), name='delete-post'),
    path('post/create/result/', views.PostCreation.as_view(), name='post-creation-result'),
]
