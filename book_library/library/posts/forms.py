from django.forms import ModelForm

from app import models


class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['content'].required = True

    class Meta:
        model = models.Post
        fields = '__all__'