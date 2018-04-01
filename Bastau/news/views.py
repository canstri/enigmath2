from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import PostForm
from .models import Post

from comments.models import Comment
from comments.forms import CommentForm

from accounts.models import Profile


def news_create(request):
    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404
        
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"
    
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    
    context = {
        "form": form,
        "staff":staff,
        "user":request.user,
        "profile":profile,
    }
    return render(request, "news_create.html", context)

def news_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)

    initial_data={
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }

    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"

    form = CommentForm(request.POST or None, initial=initial_data)

    if form.is_valid():
        content_type = ContentType.objects.get(model=form.cleaned_data.get("content_type"))
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()


        new_comment, created = Comment.objects.get_or_create(
                            user = request.user,
                            content_type= content_type,
                            object_id = obj_id,
                            content = content_data,
                            parent = parent_obj,
                        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    
    profile = 'admin'
    is_auth = False
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
        is_auth = True


    
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "comments": instance.comments,
        "comments_parents": instance.comments_parents,
        "comment_form":form,
        "post_url":instance.get_absolute_url(),
        "staff":staff,
        "profile":profile,
        "user":request.user,
        "is_auth":is_auth,
    }
    return render(request, "news_detail.html", context)

def news_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active() #.order_by("-timestamp")
    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"
        queryset_list = Post.objects.all()
    
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)|
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
                ).distinct()
    paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    likes = Post.likes
    
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    context = {
        "object_list": queryset, 
        "title": "News",
        "page_request_var": page_request_var,
        "today": today,
        "staff" : staff,
        "profile": profile,
        "user":request.user,
    }
    return render(request, "news_list.html", context)





def news_update(request, slug=None):
    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)

    context = {
        "title": instance.title,
        "instance": instance,
        "form":form,
        "user":request.user,
        "profile":profile,
    }
    return render(request, "news_create.html", context)



def news_delete(request, slug=None):
    try:
        instance = Post.objects.get(slug=slug)
    except:
        raise Http404

    if not request.user.is_staff and not request.user.is_superuser:
        reponse.status_code = 403
        return HttpResponse("You do not have permission to do this.")

    for comment in instance.comments_parents:
        comment.delete()
    for comment in instance.comments:
        comment.delete()

    if request.method == "POST":
        instance.delete()
        messages.success(request, "Successfully deleted")
        return redirect("news:list")
    context = {
        "object": instance
    }
    return render(request, "confirm_delete.html", context)