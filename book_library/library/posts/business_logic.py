from app import models

from . import forms


def get_valid_data(post, title, content):
    if title.strip() == '':
        title = post.title
    if content.strip() == '':
        content = post.content
    return title, content


def set_post_edit_context(context, **kwargs):
    context['title'] = 'Edit post'
    context['action'] = 'Edit'
    context['post'] = models.Post.objects.get(pk=kwargs.get('pk'))
    tags_sql = "SELECT id, denomination from tag WHERE id NOT IN (SELECT t.id FROM tag t " \
                f"LEFT JOIN post_tag pt ON pt.tag_id = t.id WHERE pt.post_id = {kwargs.get('pk')})"
    context['tags'] = models.Tag.objects.raw(tags_sql)
    own_tags_sql = "SELECT id, denomination from tag WHERE id IN (SELECT t.id FROM tag t " \
                    f"LEFT JOIN post_tag pt ON pt.tag_id = t.id WHERE pt.post_id = {kwargs.get('pk')})"
    context['own_tags'] = models.Tag.objects.raw(own_tags_sql)
    context['main_form'] = forms.PostForm(instance=context['post'])