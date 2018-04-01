from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from django.utils.text import slugify
from markdown_deux import markdown
from problems.models import Problem
from django.utils.safestring import mark_safe
from transliterate import translit, get_available_language_codes

class OlympManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(OlympManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    OlympModel = instance.__class__
    new_id = OlympModel.objects.order_by("id").last().id + 1
    return "%s/%s" %(instance.id, filename)

class Olymp(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete = models.PROTECT)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    draft = models.BooleanField(default=False)
    image = models.ImageField(upload_to=upload_location, 
            null=True, 
            blank=True, 
            width_field="width_field", 
            height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    start_time = models.DateField(auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = OlympManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if not self.slug:
            self.slug = slugify(translit(self.title, 'ru', reversed=True))
        return reverse("olymps:detail", kwargs={"slug": self.slug})
    
    def get_delete_url(self):
        return reverse("olymps:delete", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse("olymps:update", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["start_time", "-timestamp"]

        
    def get_author(self):
        return reverse("accounts:profile", kwargs={"user":self.user})

    @property
    def problems(self):
        qs = Problem.objects.filter_by_instance(self)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type



def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if not slug:
        slug = slugify(translit(instance.title, 'ru', reversed=True))
    if new_slug is not None:
        slug = new_slug
    qs = Olymp.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)



pre_save.connect(pre_save_post_receiver, sender=Olymp)