from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from app import models, mixins

from . import forms, business_logic

class PostsListView(ListView):
    paginate_by = 3
    model = models.Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        sql = f"SELECT p.id, p.title, p.content, p.published_date, (SELECT TOP 1 denomination from tag t INNER JOIN post_tag pt " \
               "ON t.id = pt.tag_id WHERE pt.post_id = p.id ORDER BY t.id) as tag FROM post p WHERE p.title " \
              f"LIKE '%%{search_query}%%' OR p.content LIKE '%%{search_query}%%' ORDER BY p.published_date DESC"
        posts = models.Post.objects.raw(sql)
        return posts

    def get_context_data(self, **kwargs):
        context = super(PostsListView, self).get_context_data(**kwargs)
        context['title'] = 'Home'
        context['search'] = self.request.GET.get('search', '')
        return context


class SinglePostView(DetailView):
    template_name = 'posts/post_details.html'
    model = models.Post
    pk_url_kwarg = 'pk'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(SinglePostView, self).get_context_data(**kwargs)
        context['title'] = get_object_or_404(models.Post, pk=self.kwargs['pk']).title
        sql = f"SELECT t.id, t.denomination FROM tag t INNER JOIN post_tag pt ON pt.tag_id = t.id WHERE pt.post_id = {self.kwargs['pk']}"
        context['tags'] = models.Tag.objects.raw(sql)
        return context


class PostEditView(mixins.RedirectIfNotStuff, LoginRequiredMixin, DetailView):
    template_name = 'posts/edit_post.html'
    pk_url_kwarg = 'pk'
    model = models.Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostEditView, self).get_context_data(**kwargs)
        business_logic.set_post_edit_context(context, **self.kwargs)
        return context


class PostEditing(mixins.RedirectIfNotStuff, LoginRequiredMixin, UpdateView):
    def post(self, request, *args, **kwargs):
        post = models.Post.objects.get(pk=self.kwargs.get('pk'))

        title = request.POST.get('title')
        content = request.POST.get('content')
        post.title, post.content = business_logic.get_valid_data(post, title, content)
        post.save()

        messages.success(self.request, "Post was updated successfully!")
        return redirect('post', pk=self.kwargs.get('pk'))


class TagAddingToPost(mixins.RedirectIfNotStuff, LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        post = models.Post.objects.get(pk=self.kwargs.get('pk'))
        tag = models.Tag.objects.get(pk=int(request.POST.get('tag')))

        models.PostTag.objects.create(post=post, tag=tag)
        messages.success(self.request, f"Tag { tag.denomination } was added successfully!")
        return redirect('post', pk=self.kwargs.get('pk'))


class TagDeleteFromPost(mixins.RedirectIfNotStuff, LoginRequiredMixin, DeleteView):
    def post(self, request, *args, **kwargs):
        post = models.Post.objects.get(pk=self.kwargs.get('pk'))
        tag = models.Tag.objects.get(pk=int(request.POST.get('tag')))

        post_tag = models.PostTag.objects.filter(post=post, tag=tag)
        if post_tag.exists():
            post_tag[0].delete()
        messages.success(self.request, f"Tag { tag.denomination } was deleted from this post.")
        return redirect('post', pk=self.kwargs.get('pk'))


class PostCreationView(mixins.RedirectIfNotStuff, LoginRequiredMixin, TemplateView):
    template_name = 'posts/edit_post.html'

    def get_context_data(self, **kwargs):
        context = super(PostCreationView, self).get_context_data(**kwargs)
        context['title'] = 'Post adding'
        context['action'] = 'Create'
        context['main_form'] = forms.PostForm()
        return context


class PostCreation(LoginRequiredMixin, CreateView):
    model = models.Post
    fields = ['title', 'content']

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        content = request.POST.get('content')
        sql = f"INSERT INTO post (title, content, published_date) VALUES ('{title}', '{content}', GETDATE())"

        with connection.cursor() as cursor:
            cursor.execute(sql)
            cursor.execute(f"SELECT id FROM post WHERE title = '{title}'")
            row = cursor.fetchone()

        messages.success(self.request, "Post was created successfully!")
        return redirect('post', pk=row[0])


class PostDeleteView(mixins.RedirectIfNotStuff, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    template_name = 'delete_template.html'
    model = models.Post
    success_message = "Post was deleted successfully!"

    def get_context_data(self, **kwargs):
        context = super(PostDeleteView, self).get_context_data(**kwargs)
        context['object'] = models.Post.objects.get(pk=self.kwargs.get('pk')).title
        context['type'] = 'posts'
        context['title'] = 'Deleting'
        context.update(self.kwargs)
        return context

    def post(self, request, *args, **kwargs):
        post = models.Post.objects.get(pk=self.kwargs.get('pk'))
        post.delete()
        messages.success(self.request, "Post was deleted successfully!")
        return redirect('posts')
