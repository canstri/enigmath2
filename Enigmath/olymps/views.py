from urllib.parse import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import OlympForm
from .models import Olymp

from problems.models import Problem
from problems.models import CheckProblem
from problems.forms import CreateProblemForm

from accounts.models import Profile


def olymp_create(request):
    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404
        
    form = OlympForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
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
    return render(request, "olymp_create.html", context)

def olymp_detail(request, slug=None):
    instance = get_object_or_404(Olymp, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff and not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.title)

    initial_data={
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }

    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"

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
    
    profile = 'admin'
    is_auth = False
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
        is_auth = True

    array_of_user = []
    for prblm in instance.problems:
        array_of_user.append([prblm, CheckProblem.objects.filter(user = request.user.id, problem_id = prblm.id)])

    #check_problem = CheckProblem.objects.filter(user = request.user.id)
   
    
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "array_of_user": array_of_user,
        "create_problem_form":form,
        "olymp_url":instance.get_absolute_url(),
        "staff":staff,
        "profile":profile,
        "user":request.user,
        "is_auth": is_auth,
    }
    return render(request, "olymp_detail.html", context)

def olymps_list(request):
    today = timezone.now().date()
    queryset_list = Olymp.objects.active() #.order_by("-timestamp")
    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"
        queryset_list = Olymp.objects.all()
    
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(title__icontains=query)|
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

    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    context = {
        "object_list": queryset, 
        "title": "Olympiads",
        "page_request_var": page_request_var,
        "today": today,
        "staff" : staff,
        "profile": profile,
        "user":request.user,
    }
    return render(request, "olymps_list.html", context)





def olymp_update(request, slug=None):
    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Olymp, slug=slug)
    form = OlympForm(request.POST or None, request.FILES or None, instance=instance)
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
    return render(request, "olymp_create.html", context)



def olymp_delete(request, slug=None):
    try:
        instance = Olymp.objects.get(slug=slug)
    except:
        raise Http404

    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404


    if request.method == "POST":
        for prblm in Problem.objects.filter(content_object = instance):
            for checkprblm in CheckProblem.objects.filter(problem_id = prblm.id):
                checkprblm.delete()
            prblm.delete()

        instance.delete()
        messages.success(request, "Successfully deleted")
        return redirect("olymps:list")
    context = {
        "object": instance
    }
    return render(request, "confirm_delete.html", context)