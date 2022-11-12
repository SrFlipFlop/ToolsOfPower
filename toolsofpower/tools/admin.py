from django.contrib import admin
from . import models

admin.site.register(models.Tag)
admin.site.register(models.Source)
admin.site.register(models.Platform)
admin.site.register(models.Language)
admin.site.register(models.Tool)