from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

from accounts.models import Profile
from .solve_problem_form import SaveProblemForm

from .expression_form import ExpressionForm
from .models import Problem
from .models import CheckProblem

from olymps.models import Olymp
from lemmas.isequal import isequal


def problem_delete(request, id):
    try:
        obj = Problem.objects.get(id=id)
    except:
        raise Http404

    if obj.user != request.user:
        reponse.status_code = 403
        return HttpResponse("You do not have permission to do this.")

    if request.method == "POST":
        parent_obj_url = obj.content_object.get_absolute_url()

        for checkprblm in CheckProblem.objects.filter(problem_id = obj.id):
            checkprblm.delete()

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

def problem_thread(request, id):
    try:
        obj = Problem.objects.get(id=id)
    except:
        raise Http404

    content_object = obj.content_object 
    content_id = obj.content_object.id

    initial_data = {
            "content_type": obj.content_type,
            "object_id": obj.object_id
    }

    if request.user.id:
        check_problem = CheckProblem.objects.get(problem_id = obj.id, user = request.user.id)
    else:
        messages.warning(request, "You need to authanticate to see problems")
        return HttpResponseRedirect(obj.content_object.get_absolute_url())
    
    action_check = ''
    action_check2 = ''

    
    expression_form = ExpressionForm(request.POST or None)
    
    save_problem_form = SaveProblemForm(request.POST or None)

    if len(check_problem.actions) > 0:
        if check_problem.actions[0][1] == 'f':
            check_problem.actions.pop(0) 
            check_problem.save()
    if expression_form.is_valid():
        expr_id = expression_form.cleaned_data.get('exp_id')-1
        if 'delete' in request.POST:
            check_problem.actions.pop(expr_id) 
            check_problem.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        if 'use' in request.POST:
            init_data = {
                'expr2': check_problem.actions[expr_id][0]
            }
            save_problem_form = SaveProblemForm(request.POST or None, initial = init_data)
        
    if save_problem_form.is_valid():
        expr1 = save_problem_form.cleaned_data.get('expr1')
        expr2 = save_problem_form.cleaned_data.get('expr2')
        action_check = isequal(expr1)
        if action_check == '':
            action_check2 = isequal(expr2)

        if 'save' in request.POST:
            if action_check != '':
                check_problem.actions.append([expr1, action_check])
                check_problem.save()
                return HttpResponseRedirect(obj.get_absolute_url())  
            elif action_check2 != '':
                check_problem.actions.append([expr2, action_check2])
                check_problem.save()
                return HttpResponseRedirect(obj.get_absolute_url()) 
    
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"
    
    

    context = {
        "staff":staff,
        "profile":profile,
        "problem": obj,
        "save_problem_form": save_problem_form,
        "check_problem": check_problem,
        "action_check":action_check,
        "expression_form": expression_form,
    }
    return render(request, "problem.html", context)
