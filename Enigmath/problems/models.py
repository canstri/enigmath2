from __future__ import unicode_literals

from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save
from django.utils import timezone


from django.utils.text import slugify
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from transliterate import translit, get_available_language_codes

from django.urls import reverse

from django.db import models
from django.contrib.postgres.fields import HStoreField
from django.contrib.postgres.fields import ArrayField

from accounts.models import Profile


# Create your models here.\


class ProblemManager(models.Manager):
    def all(self):
        return super(ProblemManager, self)

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return super(ProblemManager, self).filter(content_type=content_type, object_id= instance.id)

    def filter_by_author(self, author):
        return super(ProblemManager, self).filter(user=author)


class Problem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete = models.PROTECT)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null = True)
    object_id = models.PositiveIntegerField(null = True)
    content_object = GenericForeignKey('content_type', 'object_id')

    content = models.TextField()
    title = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProblemManager()

    class Meta:
        ordering = ['timestamp']

    def __unicode__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return reverse("problems:thread", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("problems:delete", kwargs={"id": self.id})
    
    def get_profile(self):
        return reverse("accounts:profile", kwargs={"user":self.user})



class CheckProblem(models.Model):
    user = models.PositiveIntegerField(null = True)
    problem_id = models.PositiveIntegerField(null = True)
    actions = ArrayField(ArrayField(models.TextField()), default=[['f', 'f']])
    solved = models.BooleanField(default=False) 


    # def delete():
    #     return reverse("problems:exp_delete")




