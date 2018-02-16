from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Course

from comments.models import Comment
from comments.forms import CommentForm

from accounts.models import Profile

from school.models import Course


def course_list(request):
    today = timezone.now().date()
    queryset_list = Course.objects.all() #.order_by("-timestamp")
    
    
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)

    context = {
        "title": "Courses",
        "profile": profile,
        "user":request.user,
    }
    return render(request, "course_list.html", context)
