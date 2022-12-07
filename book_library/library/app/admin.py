from django.contrib import admin

from . import models


admin.site.register(models.Publisher)
admin.site.register(models.Genre)
admin.site.register(models.Country)
admin.site.register(models.Review)

admin.site.register(models.Profile)
admin.site.register(models.Mailing)

admin.site.register(models.Book)
