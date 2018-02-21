from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import CourseForm
from .models import Course, PassCourse

from lectures.models import Lecture, PassLecture

from lectures.forms import LectureForm

from accounts.models import Profile




def course_create(request):
    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404
        
    form = CourseForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        for p in Profile.objects.filter():
            c = PassCourse.objects.get_or_create(
                user = p.user.id,
                course_id = instance.id,
                passed = 0,
            )

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
    return render(request, "course_create.html", context)

def course_detail(request, slug=None):
    instance = get_object_or_404(Course, slug=slug)
    if instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    share_string = quote_plus(instance.content)

    initial_data={
        "content_type": instance.get_content_type,
        "object_id": instance.id,
    }

    form = LectureForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        content_type = ContentType.objects.get(model=form.cleaned_data.get("content_type"))
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        lecture_title = form.cleaned_data.get("title")
        level = form.cleaned_data.get("level")
        new_lecture, created = Lecture.objects.get_or_create(
                            user = request.user,
                            content_type= content_type,
                            object_id = obj_id,
                            content = content_data,
                            title = lecture_title,
                            level = level,
                        )
        for p in Profile.objects.filter():
            c = PassLecture.objects.get_or_create(
                user = p.user.id,
                lecture_id = new_lecture.id,
                passed = 0,
            )
        
        #return HttpResponseRedirect(new_lecture.content_object.get_absolute_url())
    
    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"

    profile = 'admin'
    is_auth = False
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
        is_auth = True

    is_course_passed = PassCourse.objects.get(course_id = instance.id, user = request.user.id)

    x = 0
    array_of_user = []
    for lssn in instance.lectures:
        pl = PassLecture.objects.get(user = request.user.id, lecture_id = lssn.id)
        array_of_user.append([lssn, pl])
        x = x + int(pl.passed)
    percent = 0
    if len(instance.lectures) > 0:
        percent = x/(3*len(instance.lectures))
    if percent > 0 and percent < 0.3:
        is_course_passed.passed = 1
        is_course_passed.save()
    if percent >= 0.3 and percent < 0.6:
        is_course_passed.passed = 2
        is_course_passed.save()
    if percent >= 0.6:
        is_course_passed.passed = 3
        is_course_passed.save()


    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "course_url":instance.get_absolute_url(),
        "staff":staff,
        "profile":profile,
        "user":request.user,
        "is_auth":is_auth,
        "form":form,
        "is_course_passed": is_course_passed.passed,
        "array_of_user": array_of_user,
    }
    return render(request, "course_detail.html", context)

def course_list(request):
    queryset_list = Course.objects.active()
    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"
        queryset_list = Course.objects.all()
    
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
        array_of_user.append([crs, PassCourse.objects.get(user = request.user.id, course_id = crs.id)])    

    context = {
        "object_list":queryset,
        "array_of_user": array_of_user,
        "title": "Courses",
        "page_request_var": page_request_var,
        "staff" : staff,
        "profile": profile,
        "user":request.user,
    }
    return render(request, "course_list.html", context)





def course_update(request, slug=None):
    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Course, slug=slug)
    form = CourseForm(request.POST or None, request.FILES or None, instance=instance)
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
    return render(request, "course_create.html", context)



def course_delete(request, slug=None):
    try:
        instance = Course.objects.get(slug=slug)
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
        return redirect("courses:list")
    context = {
        "object": instance
    }
    return render(request, "confirm_delete.html", context)