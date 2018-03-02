from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import SetForm
from .models import Set, PassSet
from courses.models import Course

from accounts.models import Profile
from problems.models import Problem
from problems.models import CheckProblem
from problems.forms import CreateProblemForm

from .models import PassSet

def set_detail(request, id=None):
    if not request.user.is_authenticated:
        raise Http404
    instance = get_object_or_404(Set, id=id)
    share_string = quote_plus(instance.content)

    initial_data={
        "content_type": instance.get_content_type,
        "object_id": instance.id,
    }

    add_problem_form = AddProblemForm(request.POST or None, initial=initial_data)
    if add_problem_form.is_valid():
        prblm_id = add_problem_form.cleaned_data.get("prblm_id")
        instance.problem_list.append(prblm_id)

    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"

    profile = Profile.objects.get(user = request.user.id)
    number_of_solved = 0
    array_of_user = []
    for prbl_id in instance.problem_list:
        prblm = Problem.objects.get(id = prbl_id)
        cp = CheckProblem.objects.get(user = request.user.id, problem_id = prbl_id)
        array_of_user.append([prblm, cp])
        if cp.solved == True:
            number_of_solved = number_of_solved + 1

    percent = 0
    if len(instance.problems) > 0:
        percent = number_of_solved/len(instance.problems)
    pl = PassSet.objects.get(user = request.user.id, set_id = instance.id)
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
        "set_url":instance.get_absolute_url(),
        "create_problem_form":form,
        "staff":staff,
        "profile":profile,
        "user":request.user,
        "form":form,
        "pass_set":pl.passed,
        "number_of_solved": number_of_solved,
    }
    return render(request, "set_detail.html", context)


def set_delete(request, id):
    try:
        obj = Set.objects.get(id=id)
    except:
        raise Http404

    if obj.user != request.user:
        reponse.status_code = 403
        return HttpResponse("You do not have permission to do this.")

    if request.method == "POST":
        parent_obj_url = obj.content_object.get_absolute_url()
        for prblm in obj.problems:
            prblm.delete()

        for passlssn in PassSet.objects.filter(set_id = obj.id):
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