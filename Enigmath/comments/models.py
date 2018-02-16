from __future__ import unicode_literals

from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.urls import reverse

from django.db import models
from accounts.models import Profile


# Create your models here.\


class CommentManager(models.Manager):
    def all(self):
        return super(CommentManager, self)

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return super(CommentManager, self).filter(content_type=content_type, object_id= instance.id)

    def filter_by_instance_childs(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return super(CommentManager, self).filter(content_type=content_type, object_id= instance.id).exclude(parent = None)

    def filter_by_instance_parents(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return super(CommentManager, self).filter(content_type=content_type, object_id= instance.id).filter(parent = None)


    def filter_by_author(self, author):
        return super(CommentManager, self).filter(user= author)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete = models.PROTECT)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null = True)
    object_id = models.PositiveIntegerField(null = True)
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey("self", null=True, blank=True, on_delete = models.PROTECT)

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['timestamp']

    def __unicode__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return reverse("comments:thread", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("comments:delete", kwargs={"id": self.id})

    def author(self): #replies
        return Profile.objects.get(user=self.user)


    def children(self): #replies
        return Comment.objects.filter(parent=self)

    def get_profile(self):
        return reverse("accounts:profile", kwargs={"user":self.user})


    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True


