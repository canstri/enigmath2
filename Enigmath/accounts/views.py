from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

    )

from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.contrib.auth.models import User

from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from .models import Profile
from problems.models import Problem
from problems.models import CheckProblem

from comments.models import Comment



def account_view(request, user = None):
    user = User.objects.get(username = user)
    profile = Profile.objects.get(user = user)
    school = profile.school
    birthday = profile.birthdate
    rating = profile.rating
    pid = profile.id
    user_id  = profile.user_id
    image = profile.image

    problem_set = Problem.objects.filter_by_author(user)

    initial_data = {
            "school": school,
            "birthdate": birthday,
            "image":image,
    }

    form = ProfileForm(request.POST or None, request.FILES or None, initial = initial_data)


    if form.is_valid():
        profile = form.save(commit=False)
        profile.id = pid
        profile.user_id = user_id
        messages.success(request, "Successfully Updated")
        profile.save()
    
    status = "user"    
    if user.is_staff:
        status = "staff"
    
    if user.is_superuser:
        status = "superuser"
    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"

    yourprofile = 'admin'
    if request.user.is_authenticated:
        yourprofile = Profile.objects.get(user = request.user.id)
    
    context = {
        "staff":staff,
        "user":request.user,
        "profile":yourprofile, #abc
        "hisprofile": profile, #admin
        "status":status,
        "rating": rating,
        "school": profile.school,
        "birthday": profile.birthdate,
  #      "comments": profile.comments,
        "form":form,
        "problem_set":problem_set,
    }
    return render(request, "profile.html", context)

def login_view(request):
    next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect("/")
    return render(request, "form.html", {"form":form, "title": title})


def register_view(request):
    next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        password2 = form.cleaned_data.get('password2')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)

        for prblm in Problem.objects.filter():
            c = CheckProblem.objects.get_or_create(
                user = user.id,
                problem_id = prblm.id,
                solved = False,
            )

        if next:
            return redirect(next)
        return redirect("/")

    context = {
        "form": form,
        "title": title
    }
    return render(request, "form.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")