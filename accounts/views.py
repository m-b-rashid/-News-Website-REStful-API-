from django.contrib.auth import (authenticate, get_user_model, login, logout, )
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from .forms import UserLoginForm, UserRegistrationForm
from .models import User

def login_view(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    user = authenticate(email=email, password=password)
	#send json info about user to login section of navbar with ajax
    if user:
        login(request, user)
        user_record = User.objects.filter(email = email)
        json_result = serializers.serialize('json', user_record, fields=('name'))
        return JsonResponse(json_result, DjangoJSONEncoder, False)

def register_view(request):
    title = "Register"
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST or None)
        if user_form.is_valid():
		#ensure SHA256 password encryption + save user-info
            user = user_form.save(commit=False)	
            user.set_password(request.POST["password"])
            user.save()
            messages.success(request, ('You have successfully registered!'))
            return redirect("articles:list")
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserRegistrationForm(request.POST or None)
    return render(request, "login_form.html", {
        'user_form': user_form,
        'title' : title,
    })

def logout_view(request):
    logout(request)
    return redirect("articles:list")

def like_view(request):
    return render(request, "login_form.html", {})

def profile_view(request):
    title = "Update Profile"
    if not request.user.is_authenticated():
        messages.error(request, ('You are not logged in or registered.'))
        return redirect("articles:list")
    else:
        if request.method == 'POST':
            user_form = UserRegistrationForm(data=request.POST or None, instance=request.user)
            if user_form.is_valid():
			#ensure SHA256 password encryption + save user-info
                user = user_form.save(commit=False)
                user.set_password(request.POST["password"])
                user.save()
                messages.success(request, ('You have successfully updated your profile!'))
                return redirect("articles:list")
            else:
                messages.error(request, ('Please correct the error below.'))
        else:
            user_form = UserRegistrationForm(data=request.GET or None, instance=request.user)
            return render(request, "login_form.html", {
                'user_form': user_form,
                'title': title,
            })

