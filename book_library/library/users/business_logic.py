from datetime import datetime
from app import models

from . import forms


def get_amount_of_created_stuff():
    amount = dict()

    amount['posts_amount'] = models.Post.objects.all().count()
    amount['tags_amount'] = models.Tag.objects.all().count()
    amount['books_amount'] = models.Book.objects.all().count()
    amount['genres_amount'] = models.Genre.objects.all().count()
    amount['authors_amount'] = models.Author.objects.all().count()
    amount['publishers_amount'] = models.Publisher.objects.all().count()
    return amount


def save_user_changes(profile, request):
    user_email = request.POST.get('email')
    user_first_name = request.POST.get('first_name')
    user_last_name = request.POST.get('last_name')

    if models.Mailing.objects.filter(email=profile.user.email).exists():
        if profile.user.email != user_email:
            models.Mailing.objects.get(email=profile.user.email).delete()

    profile.user.email = user_email
    profile.user.first_name = user_first_name
    profile.user.last_name = user_last_name
    profile.user.save()


def save_profile_changes(profile, request):
    profile_description = request.POST.get('description')
    profile_birth_date = None

    if request.POST.get('birth_date'):
        print(request.POST.get('birth_date'))
        profile_birth_date = datetime.strptime(request.POST.get('birth_date'), '%Y-%m-%d')

    profile_social_telegram = request.POST.get('social_telegram')
    profile_social_twitter = request.POST.get('social_twitter')
    profile_social_facebook = request.POST.get('social_facebook')

    tmp_country = request.POST.get('user_country')
    if tmp_country.strip() != '':
        country, created = models.Country.objects.get_or_create(name=tmp_country)
        profile.country = country

    profile.description = profile_description
    profile.birth_date = profile_birth_date
    profile.social_telegram = profile_social_telegram
    profile.social_twitter = profile_social_twitter
    profile.social_facebook = profile_social_facebook

    profile.save()


def set_management_context(context):
    context['title'] = 'Management Panel'
    context['tag_form'] = forms.TagForm()
    context['tags'] = models.Tag.objects.all().order_by('denomination')
    context['genre_form'] = forms.GenreForm()
    context['genres'] = models.Genre.objects.all().order_by('denomination')
    context['authors'] = models.Author.objects.all().order_by('first_name')
    context['publishers'] = models.Publisher.objects.all().order_by('denomination')
    context['publisher_form'] = forms.PublisherForm()
    context['last_post'] = models.Post.objects.order_by('-id').first()
    context['last_book'] = models.Book.objects.order_by('-id').first()
    context['reviews'] = models.Review.objects.filter(moderated=False)
    context['reviews_to_confirm'] = context['reviews'].count()
    context['emails'] = models.Mailing.objects.all().count()


def get_author_data_from_get_request(request):
    first_name = request.POST.get('first_name')
    second_name = request.POST.get('second_name')
    gender = request.POST.get('gender')
    birth_date = request.POST.get('birth_date')
    biography = request.POST.get('biography')
    return first_name, second_name, gender, birth_date, biography


def set_action(request):
    action = request.GET.get('action', 'Action')
    if action not in ['Action', 'Update', 'Insert', 'Delete']:
        action = 'Action'
    return action
