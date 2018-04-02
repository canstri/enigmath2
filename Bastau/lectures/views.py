from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import LectureForm
from .models import Lecture, PassLecture
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
        new_problem = Problem.objects.create(
                            user = request.user,
                            content_type= content_type,
                            object_id = obj_id,
                            content = content_data,
                            title = problem_title,
                        )
        for p in Profile.objects.filter():
            check_problem = CheckProblem.objects.create(
                user = p.user.id,
                problem_id = new_problem.id,
                solved = False,
            )
            check_problem.actions = []
            counter1 = 0
            counter2 = 0
            temp_str1 = ''
            temp_str2 = ''
            for i in range(0, len(new_problem.content)):
                if new_problem.content[i] == '$':
                    counter1 += 1
                if counter1 % 2 == 1:    
                    temp_str1 += new_problem.content[i]
                if counter1 % 2 == 0 and counter1 > 0:
                    temp_str1 = temp_str1[1:]
                    check_problem.actions.append([temp_str1, 'Correct'])
                    temp_str1 = ''
                    counter1 = 0

                if new_problem.content[i] == '!':
                    counter2 += 1
                if counter2 % 2 == 1:    
                    temp_str2 += new_problem.content[i]
                if counter2 % 2 == 0 and counter2 > 0:
                    temp_str2 = temp_str2[1:]
                    check_problem.actions.append([temp_str2, 'Need to prove'])
                    temp_str2 = ''
                    counter2 = 0
            check_problem.save()
        return HttpResponseRedirect(new_problem.content_object.get_absolute_url())

    
    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"

    profile = 'admin'
    is_auth = False
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
        is_auth = True

    number_of_solved = 0
    array_of_user = []
    for prblm in instance.problems:
        cp = CheckProblem.objects.get(user = request.user.id, problem_id = prblm.id)
        array_of_user.append([prblm, cp])
        if cp.solved == True:
            number_of_solved = number_of_solved + 1

    percent = 0
    if len(instance.problems) > 0:
        percent = number_of_solved/len(instance.problems)
    pl = PassLecture.objects.get(user = request.user.id, lecture_id = instance.id)
    if percent > 0 and percent < 0.3:
        pl.passed = 1
        pl.save()
    if percent >= 0.3 and percent < 0.6:
        pl.passed = 2
        pl.save()
    if percent >= 0.6:
        pl.passed = 3
        pl.save()




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
        "pass_lecture":pl.passed,
        "number_of_solved": number_of_solved,
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