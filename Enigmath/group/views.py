from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import GroupForm
from .models import Group

from lectures.models import Lecture, PassLecture

from lectures.forms import LectureForm

from accounts.models import Profile


def group_create(request):
    if not request.user.is_authenticated:
        raise Http404
        
    form = GroupForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"
    
    profile = Profile.objects.get(user = request.user.id)
    
    context = {
        "form": form,
        "staff":staff,
        "user":request.user,
        "profile":profile,
    }
    return render(request, "group_create.html", context)

def group_detail(request, slug=None):
    if not request.user.is_authenticated:
        raise Http404

    instance = get_object_or_404(Group, slug=slug)
    
    share_string = quote_plus(instance.content)

    initial_data={
        "content_type": instance.get_content_type,
        "object_id": instance.id,
    }

    form = SetForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        content_type = ContentType.objects.get(model=form.cleaned_data.get("content_type"))
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        set_title = form.cleaned_data.get("title")
        level = form.cleaned_data.get("level")
        new_set = Set.objects.get_or_create(
                            user = request.user,
                            content_type= content_type,
                            object_id = obj_id,
                            content = content_data,
                            title = set_title,
                            level = level,
                        )
        for group_user_id in instance.user_list:
            group_user = Profile.objects.get(id = group_user_id)
            c = PassSet.objects.get_or_create(
                user = p.user.id,
                lecture_id = new_lecture.id,
                passed = 0,
            )

    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"

    profile = 'admin'
    is_auth = False
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
        is_auth = True

    is_group_passed = PassGroup.objects.get(group_id = instance.id, user = request.user.id)

    x = 0
    array_of_user = []
    for lssn in instance.lectures:
        pl = PassLecture.objects.get(user = request.user.id, lecture_id = lssn.id)
        x = x + int(pl.passed)
        array_of_user.append([lssn, pl, x])
        
    percent = 0
    if len(instance.lectures) > 0:
        percent = x/(3*len(instance.lectures))
    if percent > 0 and percent < 0.3:
        is_group_passed.passed = 1
        is_group_passed.save()
    if percent >= 0.3 and percent < 0.6:
        is_group_passed.passed = 2
        is_group_passed.save()
    if percent >= 0.6:
        is_group_passed.passed = 3
        is_group_passed.save()

    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "group_url":instance.get_absolute_url(),
        "staff":staff,
        "profile":profile,
        "user":request.user,
        "is_auth":is_auth,
        "form":form,
        "is_group_passed": is_group_passed.passed,
        "array_of_user": array_of_user,
    }
    return render(request, "group_detail.html", context)

def group_list(request):
    if not request.user.is_authenticated:
        raise Http404

    queryset_list = Group.objects.active()
    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"
        queryset_list = Group.objects.all()
    
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)
                ).distinct()
    paginator = Paginator(queryset_list, 10)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    
    array_of_user = []
    for crs in queryset_list:
        array_of_user.append([crs, PassGroup.objects.get(user = request.user.id, group_id = crs.id)])    

    context = {
        "object_list":queryset,
        "array_of_user": array_of_user,
        "title": "Groups",
        "page_request_var": page_request_var,
        "staff" : staff,
        "profile": profile,
        "user":request.user,
    }
    return render(request, "group_list.html", context)





def group_update(request, slug=None):
    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Group, slug=slug)
    form = GroupForm(request.POST or None, request.FILES or None, instance=instance)
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
    return render(request, "group_create.html", context)



def group_delete(request, slug=None):
    try:
        instance = Group.objects.get(slug=slug)
    except:
        raise Http404

    if not request.user.is_staff and not request.user.is_superuser:
        reponse.status_code = 403
        return HttpResponse("You do not have permission to do this.")


    if request.method == "POST":
        for lecture in instance.lectures:
            lecture.delete()
        instance.delete()
        messages.success(request, "Successfully deleted")
        return redirect("groups:list")
    context = {
        "object": instance
    }
    return render(request, "confirm_delete.html", context)