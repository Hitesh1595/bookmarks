from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from account.forms import LoginForm
from django.contrib import messages

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from account.models import Contact

def user_follow(request):
    user_id = request.POST.get("id")
    action = request.POST.get("action")
    if user_id and action:
        try:
            user = User.objects.get(id = user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_form = request.user,user_to = user)
            else:
                Contact.objects.filter(user_form = request.user,user_to = user).delete()
            return JsonResponse({"status":'ok'})
        except User.DoesNotExist:
            return JsonResponse({"status":'error'})
    return JsonResponse({"status":"error"})

@login_required
def user_list(request):
    users = User.objects.filter(is_active = True)
    return render(request,'account/user/list.html',{'section':'people',"users":users})

@login_required
def user_details(request,username):
    user = get_object_or_404(User,username = username,is_active = True)
    return render(request,'account/user/detail.html',{'section':'people','user':user})

# Create your views here.


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated successfuly")
                else:
                    return HttpResponse("Disabled Account")
            else:
                return HttpResponse("Invalid User")
    else:
        form = LoginForm

    context = {"form": form}

    return render(request, "account/login.xhtml", context=context)


@login_required
def dashboard(request):
    context = {"section": "dashboard"}

    return render(request, "account/dashboard.html", context=context)


from django.contrib.auth import logout

# def logout_view(request):
#     logout(request)
#     return render(request,'account/logged_out.html')

from account.forms import UserRegistrationForm
from .models import Profile
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # craeate new user object but avoid saving it yet
            new_user = user_form.save(commit = False)
            # set the chosen password
            # set_pasword handle the password in hash bebore saving into database
            new_user.set_password(user_form.cleaned_data['password'])

            # save the user object
            new_user.save()
            # Create the User Profile
            Profile.objects.create(user=new_user)

            return render(request,'account/registration_done.html',{'new_user':new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request,'account/register.html',{'user_form':user_form})

from account.forms import UserEditForm,ProfileEditForm
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data = request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data = request.POST,files = request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Profile updated \
                                        succesfully')
        else:
            messages.error(request,'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user) 
        profile_form = ProfileEditForm(instance = request.user.profile)
      


    
    context = {
        'user_form':user_form,
        'profile_form':profile_form
    }
    return render(request,'account/edit.html',context=context)