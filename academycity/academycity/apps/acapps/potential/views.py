from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from ...webcompanies.WebCompanies import WebSiteCompany
from ...users.forms import (RegistrationForm, ACAuthenticationForm)
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from ...core.utils import log_debug
from django.urls import reverse
from ...core.apps_general_functions import activate_obj_function


#             messages.error(request, "Invalid username or password.")


def home(request):
    if request.method == "POST":
        form_login = ACAuthenticationForm(request, data=request.POST)
        if form_login.is_valid():
            username = form_login.cleaned_data.get('username')
            password = form_login.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return home_logged(request)
        else:
            return signup_login_form(request, error_message="Invalid username or password.")
    return signup_login_form(request, error_message='')


def signup_login_form(request, error_message=''):
    form_login = ACAuthenticationForm()
    form_signup = RegistrationForm()
    arg = {'form_login': form_login, 'form_signup': form_signup, 'error_message': error_message,
           'redirect_field_name': "next", 'redirect_field_value': reverse('potential:home')
           }
    return render(request, 'potential/login_page.html', arg)


def home_logged(request):
    wsc = WebSiteCompany(request, web_company_id=21, is_test=True)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id

    # print(request.user.groups.all().values()) #  .filter(name=group_name).exists()
    app_name = "default"
    if request.user.groups.filter(name="training-admin").exists():
        app_name = "admin"
    elif request.user.groups.filter(name="training-soldier").exists():
        app_name = "soldier"
    return app_id(request, app_name, company_obj_id_)


def app_id(request, app_name, company_obj_id):
    company_obj_id_ = company_obj_id
    app_ = "potential"
    app_activate_function_link_ = reverse(app_+':activate_obj_function', kwargs={})
    return render(request, app_+'//home.html', {"atm_name": app_+"_"+app_name+"_atm",
                                                "app": app_,
                                                "app_activate_function_link": app_activate_function_link_,
                                                "company_obj_id": company_obj_id_,
                                                "title": app_}
                  )


def app(request, app_name):
    wsc = WebSiteCompany(request, web_company_id=21, is_test=True)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id
    return app_id(request, app_name, company_obj_id_)
