from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from ...webcompanies.WebCompanies import WebSiteCompany
from ...users.forms import (RegistrationForm, ACAuthenticationForm)
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from ...core.utils import log_debug
from django.urls import reverse
from ...core.apps_general_functions import activate_obj_function
from ...core.utils import log_debug, clear_log_debug


def home(request):
    # print("66-0")

    log_debug("training home : 60-0")
    wsc = WebSiteCompany(request, web_company_id=20)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id
    log_debug("training home : 60-00: company_obj_id_: "+str(company_obj_id_))
    app_name = "login"
    return app_id(request, app_name, company_obj_id_)

    #
    # if request.method == "POST":
    #     form_login = ACAuthenticationForm(request, data=request.POST)
    #     if form_login.is_valid():
    #         username = form_login.cleaned_data.get('username')
    #         password = form_login.cleaned_data.get('password')
    #
    #         user = authenticate(username=username, password=password)
    #         if user is not None:
    #             login(request, user)
    #             messages.info(request, f"You are now logged in as {username}.")
    #             return home_logged(request)
    #             # redirect("training:home_logged")
    #     else:
    #         return signup_login_form(request, error_message="Invalid username or password.")
    # elif request.user.is_authenticated:
    #     home_logged(request)
    # return signup_login_form(request, error_message='')

# def signup_login_form(request, error_message=''):
#     form_login = ACAuthenticationForm()
#     form_signup = RegistrationForm()
#     arg = {'form_login': form_login, 'form_signup': form_signup, 'error_message': error_message,
#            'redirect_field_name': "next", 'redirect_field_value': reverse('training:home')
#            }
#     return render(request, 'training/login_page.html', arg)
#
# def home_logged(request):
#     log_debug("home_logged")
#     print("home_logged")
#     # try:
#     #     logout()
#     # except Exception as ex:
#     #     pass
#     wsc = WebSiteCompany(request, web_company_id=20)
#     company_obj = wsc.site_company()
#     company_obj_id_ = company_obj.id
#
#     # print(request.user.groups.all().values()) #  .filter(name=group_name).exists()
#     app_name = "default"
#     print(request.user)
#     if request.user.groups.filter(name="t_senior_manager").exists():
#         app_name = "senm"
#     elif request.user.groups.filter(name="t_admin").exists():
#         app_name = "admin"
#     log_debug(app_name)
#
#     print(app_name)
#     print(app_name)
#
#     return app_id(request, app_name, company_obj_id_)
#
# def homet(request):
#     if not request.user.is_authenticated:
#         return signup_login_form(request, error_message='You need to login')
#     wsc = WebSiteCompany(request, web_company_id=20, is_test=True)
#     company_obj = wsc.site_company()
#     company_obj_id_ = company_obj.id
#     app_name = "default"
#     return app_id(request, app_name, company_obj_id_)

#

def app_id(request, app_name, company_obj_id):
    # print("66-01", app_name)
    log_debug("training home : 60-03: "+app_name)
    try:
        if request.user.is_anonymous:
            user_id = -1
            app_name = "login"
            # print("not login")
        else:
            user_id = request.user.id
            user_ = request.user
            default_battalion = user_.training_user_instructors.default_battalion
            if request.user.groups.filter(name="t_senior_manager").exists():
                app_name = "senm"
            elif request.user.groups.filter(name="t_admin").exists():
                app_name = "tadmin"
            elif request.user.groups.filter(name="admins").exists():
                # app_name = "admin"
                log_debug("training home : 60-04: "+app_name)
                pass
            else:
                app_name = "default"
            # print(app_name)

    except Exception as ex:
        print(ex)
    # print("66-015", app_name, user_id)
    company_obj_id_ = company_obj_id
    app_ = "training"
    log_debug("app_id 60-05: app_name=" + app_name + ", app_="  + app_ + ", company_obj_id_= " + str(company_obj_id_))

    app_activate_function_link_ = reverse(app_+':activate_obj_function', kwargs={})
    logmein_link_ = reverse(app_+':logmein', kwargs={})
    # log_debug("app_activate_function_link_=" + app_activate_function_link_)
    # log_debug("logmein_link_=" + logmein_link_)
    return render(request, app_+'//home.html', {"atm_name": app_+"_"+app_name+"_atm",
                                                "app": app_,
                                                "logmein_link":logmein_link_,
                                                "app_activate_function_link": app_activate_function_link_,
                                                "company_obj_id": company_obj_id_,
                                                "user_id":user_id, "default_battalion":default_battalion,
                                                "title": app_}
                  )


def appt(request, app_name):
    log_debug("training appt: 60-03: "+app_name)
    wsc = WebSiteCompany(request, web_company_id=20, is_test=True)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id
    return app_id(request, app_name, company_obj_id_)


def app(request, app_name):
    log_debug("training app: 60-02: "+app_name)
    wsc = WebSiteCompany(request, web_company_id=20)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id
    return app_id(request, app_name, company_obj_id_)
