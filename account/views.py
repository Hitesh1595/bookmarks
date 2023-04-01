from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from account.forms import LoginForm

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

            return render(request,'account/registration_done.html',{'new_user':new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request,'account/register.html',{'user_form':user_form})