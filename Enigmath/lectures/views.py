from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import LectureForm
from .models import Lecture
from courses.models import Course

from accounts.models import Profile
from problems.models import Problem
from problems.models import CheckProblem
from problems.forms import CreateProblemForm

from .models import PassLecture

def lecture_detail(request, id=None):
    instance = get_object_or_404(Lecture, id=id)
    if instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    share_string = quote_plus(instance.content)

    initial_data={
        "content_type": instance.get_content_type,
        "object_id": instance.id,
    }

    form = CreateProblemForm(request.POST or None, initial=initial_data)

    if form.is_valid():
        content_type = ContentType.objects.get(model=form.cleaned_data.get("content_type"))
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        problem_title = form.cleaned_data.get("title")
        new_problem, created = Problem.objects.get_or_create(
                            user = request.user,
                            content_type= content_type,
                            object_id = obj_id,
                            content = content_data,
                            title = problem_title,
                        )
        for p in Profile.objects.filter():
            c = CheckProblem.objects.get_or_create(
                user = p.user.id,
                problem_id = new_problem.id,
                solved = False,
            )
        return HttpResponseRedirect(new_problem.content_object.get_absolute_url())

    
    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"

    profile = 'admin'
    is_auth = False
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
        is_auth = True

    array_of_user = []
    for prblm in instance.problems:
        array_of_user.append([prblm, CheckProblem.objects.filter(user = request.user.id, problem_id = prblm.id)])

    context = {
        "instance": instance,
        "share_string": share_string,
        "array_of_user": array_of_user,
        "lecture_url":instance.get_absolute_url(),
        "create_problem_form":form,
        "staff":staff,
        "profile":profile,
        "user":request.user,
        "is_auth":is_auth,
        "form":form,
    }
    return render(request, "lecture_detail.html", context)


def lecture_delete(request, id):
    try:
        obj = Lecture.objects.get(id=id)
    except:
        raise Http404

    if obj.user != request.user:
        reponse.status_code = 403
        return HttpResponse("You do not have permission to do this.")

    if request.method == "POST":
        parent_obj_url = obj.content_object.get_absolute_url()
        for prblm in obj.problems:
            prblm.delete()

        for passlssn in PassLecture.objects.filter(lecture_id = obj.id):
            passlssn.delete()

        obj.delete()
        messages.success(request, "This has been deleted.")
        return HttpResponseRedirect(parent_obj_url)
    
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    staff = "no"

    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"

    context = {
        "staff":staff,
        "profile":profile,
        "object": obj,
    }
    return render(request, "confirm_delete.html", context)