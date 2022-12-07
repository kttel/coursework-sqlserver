from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView, DeleteView, UpdateView, View
from django.urls import reverse_lazy
from django.db import connection
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from app import models, mixins

from . import forms
from .business_logic import (
    get_amount_of_created_stuff,
    save_user_changes,
    save_profile_changes,
    set_management_context,
    get_author_data_from_get_request,
    set_action,
)


class UserLoginView(LoginView):
    template_name = 'users/login_register.html'
    form_class = forms.CustomAuthForm
    success_url = 'posts'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('posts')
        return super(UserLoginView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data(**kwargs)
        context['action'] = 'login'
        return context


class UserRegisterView(CreateView):
    template_name = 'users/login_register.html'
    form_class = forms.RegisterForm
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        context['action'] = 'register'
        return context

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('posts')
        return super().get(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
    model = models.Profile
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['title'] = 'My profile'
        context['profile'] = models.Profile.objects.get(pk=self.request.user.profile.pk)
        context['mailing_record_exists'] = models.Mailing.objects.filter(email=self.request.user.email).exists()
        return context


class EmailAdding(LoginRequiredMixin, CreateView):
    template_name = 'blank.html'
    model = models.Mailing
    fields = ['email']

    def post(self, request, *args, **kwargs):
        messages.success(self.request, "E-mail was added to mailing list!")
        return super(EmailAdding, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('profile')


class ManagementPanelView(mixins.RedirectIfNotStuff, LoginRequiredMixin, TemplateView):
    template_name = 'users/management_panel.html'

    def get_context_data(self, **kwargs):
        context = super(ManagementPanelView, self).get_context_data(**kwargs)
        set_management_context(context)

        for key, value in get_amount_of_created_stuff().items():
            context[key] = value
        return context


class CreateTagView(mixins.RedirectIfNotStuff, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = models.Tag
    fields = ['denomination']
    success_url = reverse_lazy('management_panel')
    success_message = 'Tag was created successfully!'


class CreateGenreView(mixins.RedirectIfNotStuff, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = models.Genre
    fields = ['denomination']
    success_url = reverse_lazy('management_panel')
    success_message = 'Genre was created successfully!'


class DeleteTagView(mixins.RedirectIfNotStuff, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = models.Tag
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('management_panel')
    template_name = 'delete_template.html'
    success_message = 'Tag was deleted successfully!'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class DeleteGenreView(mixins.RedirectIfNotStuff, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = models.Genre
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('management_panel')
    template_name = 'delete_template.html'
    success_message = 'Genre was deleted successfully!'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CreateAuthorView(mixins.RedirectIfNotStuff, LoginRequiredMixin, TemplateView):
    template_name='users/author-edit.html'

    def get_context_data(self, **kwargs):
        context = super(CreateAuthorView, self).get_context_data(**kwargs)
        context['title'] = 'Author adding'
        context['action'] = 'Create'
        context['main_form'] = forms.AuthorForm()
        return context


class CreateAuthor(mixins.RedirectIfNotStuff, LoginRequiredMixin, CreateView):
    model = models.Author
    fields = ['first_name', 'second_name', 'gender', 'birth_date', 'country', 'biography']

    def post(self, request, *args, **kwargs):
        first_name, second_name, gender, birth_date, biography = get_author_data_from_get_request(request)

        tmp_country = request.POST.get('country')
        country, created = models.Country.objects.get_or_create(name=tmp_country)

        sql = "INSERT INTO author (first_name, second_name, gender, birth_date, country, biography) " \
             f"VALUES (%s, %s, '{gender}', '{birth_date}', {country.id}, %s)"

        with connection.cursor() as cursor:
            cursor.execute(sql, [first_name, second_name, biography])

        messages.success(self.request, f"Author {first_name} {second_name} was added successfully!")
        return redirect('management_panel')


class EditAuthorView(mixins.RedirectIfNotStuff, LoginRequiredMixin, TemplateView):
    template_name = 'users/author-edit.html'

    def get_context_data(self, **kwargs):
        context = super(EditAuthorView, self).get_context_data(**kwargs)
        author = models.Author.objects.get(pk=self.kwargs.get('pk'))
        context['author'] = author
        context['title'] = 'Edit author'
        context['action'] = 'Edit'
        context['country'] = author.country.name
        context['main_form'] = forms.AuthorForm(instance=author)
        return context


class EditAuthor(mixins.RedirectIfNotStuff, LoginRequiredMixin, UpdateView):
    def post(self, request, *args, **kwargs):
        author = models.Author.objects.get(pk=self.kwargs.get('pk'))
        first_name, second_name, gender, birth_date, biography = get_author_data_from_get_request(request)

        tmp_country = request.POST.get('new_country')
        if tmp_country.strip() == '':
            tmp_country = author.country.name

        country, created = models.Country.objects.get_or_create(name=tmp_country)

        sql = f"UPDATE author SET first_name = %s, second_name = %s, " \
              f"gender = '{gender}', birth_date = '{birth_date}', biography = %s, " \
              f"country = {country.id} WHERE id = {author.id}"

        with connection.cursor() as cursor:
            cursor.execute(sql, [first_name, second_name, biography])

        messages.success(self.request, "Author was updated successfully!")
        return redirect('management_panel')


class DeleteAuthorView(mixins.RedirectIfNotStuff, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = models.Author
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('management_panel')
    template_name = 'delete_template.html'
    success_message = 'Author was deleted successfully!'


class CreatePublisherView(mixins.RedirectIfNotStuff, SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = models.Publisher
    fields = ['denomination']
    success_url = reverse_lazy('management_panel')
    success_message = 'Publisher was created successfully!'


class DeletePublisherView(mixins.RedirectIfNotStuff, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = models.Publisher
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('management_panel')
    template_name = 'delete_template.html'
    success_message = 'Publisher was deleted successfully!'


class ProfileEditingView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile-edit.html'
    context_object_name = 'profile'

    def post(self, request, *args, **kwargs):
        profile = models.Profile.objects.get(user=self.request.user)

        save_user_changes(profile, request)
        save_profile_changes(profile, request)

        messages.success(self.request, "Profile was updated successfully!")
        return redirect('profile')

    def get_context_data(self, **kwargs):
        context = super(ProfileEditingView, self).get_context_data(**kwargs)
        profile = models.Profile.objects.get(user=self.request.user)
        context['title'] = 'Profile editing'
        context['user_form'] = forms.UserForm(instance=profile.user)
        context['profile_form'] = forms.ProfileForm(instance=profile)
        if profile.country is not None:
            context['country'] = profile.country.name
        return context

    def get_queryset(self):
        profile = models.Profile.objects.get(user=self.request.user)
        return profile


class DeleteUnconfirmedReview(mixins.RedirectIfNotStuff, SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = models.Review
    pk_url_kwarg = 'pk'
    template_name = 'delete_template.html'
    success_url = reverse_lazy('management_panel')
    success_message = "Review was deleted successfully!"

    def post(self, request, *args, **kwargs):
        if self.request.GET.get('warning', '') == '1':
            review = models.Review.objects.get(pk=self.kwargs.get('pk'))
            review.profile.warnings_amount += 1
            review.profile.save()

        return super(DeleteUnconfirmedReview, self).post(request, *args, **kwargs)


class ConfirmReview(mixins.RedirectIfNotOwnReview, LoginRequiredMixin, UpdateView):
    model = models.Review
    pk_url_kwarg = 'pk'
    fields = ['moderated']

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        review = models.Review.objects.get(pk=self.kwargs.get('pk'))
        review.moderated = 1
        review.save()

        messages.success(self.request, "Review was confirmed successfully!")
        return redirect('book', pk=review.book.pk)


class ConfirmAllReviews(mixins.RedirectIfNotStuff, LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute('EXEC confirmReviews')

        messages.success(self.request, "All review from users without warnings were confirmed!")
        return redirect('management_panel')


class GetPublisherBooksAmount(mixins.RedirectIfNotStuff, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        publisher = models.Publisher.objects.get(pk=int(self.request.GET.get('publisher')))
        with connection.cursor() as cursor:
            cursor.execute(f"DECLARE @result INT; EXEC getBookAmountByPublisher @publisher_id = {publisher.pk}, " \
                            "@quantity = @result OUTPUT; SELECT @result AS amount")
            amount = cursor.fetchone()[0]
        messages.info(request, f"Books of \"{publisher.denomination}\": {amount}")
        return redirect('management_panel')


class GetLastLog(mixins.RedirectIfNotStuff, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        action = set_action(self.request)

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM getLastLog('{action}')")
            result = cursor.fetchone()

        message = f"{result[1].strftime('%m/%d/%Y, %H:%M:%S')}: [{result[2]}, {result[3]}] {result[5]}"
        messages.info(request, message)
        return redirect('management_panel')