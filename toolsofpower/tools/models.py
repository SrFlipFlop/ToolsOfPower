from uuid import uuid4

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Tag(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Source(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Platform(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Tool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    source =models.ForeignKey(Source, on_delete=models.PROTECT, blank=True, null=True)
    used = models.BooleanField(default=False)
    rating = models.FloatField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT, blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=models.PROTECT, blank=True, null=True)
    related = models.ManyToManyField('self', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name