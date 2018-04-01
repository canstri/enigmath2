from django.shortcuts import render, redirect
from accounts.models import Profile





def main_view(request):
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    
    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"
    context = {
    	"staff":staff,
	    "user":request.user,
        "profile":profile,
    }
    return render(request, "main.html", context)


def contacts_view(request):
    profile = 'admin'
    if request.user.is_authenticated:
        profile = Profile.objects.get(user = request.user.id)
    
    staff = "no"
    if request.user.is_staff or request.user.is_superuser:
        staff = "yes"
    context = {
        "staff":staff,
        "user":request.user,
        "profile":profile,
    }
    return render(request, "contacts.html", context)
