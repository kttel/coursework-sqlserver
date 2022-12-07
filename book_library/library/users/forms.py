from datetime import date
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.forms import widgets
from django.contrib.auth.models import User

from app import models


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=widgets.TextInput(attrs={'placeholder': 'Enter your username'}))
    password = forms.CharField(widget=widgets.PasswordInput(attrs={'placeholder': '••••••••••••'}))


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=widgets.TextInput(attrs={'placeholder': 'Enter your new username'}))
    password1 = forms.CharField(label='Password', widget=widgets.PasswordInput(attrs={'placeholder': 'Enter your new password'}))
    password2 = forms.CharField(label='Password confirmation', widget=widgets.PasswordInput(attrs={'placeholder': 'Repeat your password'}))
    email = forms.CharField(label='E-mail', widget=widgets.EmailInput(attrs={'placeholder': 'Enter your valid e-mail'}))


class TagForm(forms.ModelForm):
    denomination = forms.CharField(label='Denomination', widget=widgets.TextInput(attrs={'placeholder': 'Enter a new tag to add'}))

    class Meta:
        model = models.Tag
        fields = '__all__'


class GenreForm(forms.ModelForm):
    denomination = forms.CharField(label='Denomination', widget=widgets.TextInput(attrs={'placeholder': 'Enter a new genre to add'}))

    class Meta:
        model = models.Genre
        fields = '__all__'


class AuthorForm(forms.ModelForm):
    first_name = forms.CharField(label='First name', widget=widgets.TextInput(attrs={'placeholder': 'Enter author''s first name'}))
    second_name = forms.CharField(label='Second name', widget=widgets.TextInput(attrs={'placeholder': 'Enter author''s second name'}))
    biography = forms.CharField(label='Biography', widget=widgets.Textarea(attrs={'placeholder': 'Enter some information about author'}))
    country = forms.CharField(label='Country', widget=forms.TextInput(attrs={'placeholder': 'Enter author''s country'}))
    birth_date = forms.DateField(label='Date of birth', widget=forms.DateInput(attrs={'type': 'date', 'max': date.today()}))

    class Meta:
        model = models.Author
        fields = '__all__'


class PublisherForm(forms.ModelForm):
    denomination = forms.CharField(label='Denomination', widget=widgets.TextInput(attrs={'placeholder': 'Enter a new publisher to add'}))

    class Meta:
        model = models.Publisher
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ProfileForm(forms.ModelForm):
    country = forms.CharField(label='Country', widget=forms.TextInput(attrs={'placeholder': 'Enter your country'}))
    birth_date = forms.DateField(label='Date of birth', widget=forms.DateInput(attrs={'type': 'date', 'max': date.today()}))

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].required = False
        self.fields['country'].required = False

    class Meta:
        model = models.Profile
        fields = ['description', 'country', 'birth_date', 'social_telegram', 'social_twitter', 'social_facebook']
