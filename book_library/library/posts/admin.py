from django.contrib import admin
from app.models import Tag, PostTag, BookAuthor


admin.site.register(Tag)
admin.site.register(PostTag)
admin.site.register(BookAuthor)
