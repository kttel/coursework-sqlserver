from django import forms
from django.forms import widgets

from app import models


class BookForm(forms.ModelForm):
    img = forms.ImageField(label='Book image', widget=widgets.FileInput, required=False)

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['synopsis'].required = True

    class Meta:
        model = models.Book
        fields = '__all__'


class ReviewForm(forms.ModelForm):
    vote = forms.CharField(label='Vote',
                           widget=widgets.RadioSelect(choices=(('up', 'Up vote'), ('down', 'Down vote')),
                                                      attrs={'class': 'inline_select'}),
                           required=False)

    class Meta:
        model = models.Review
        fields = ['title', 'content', 'vote']