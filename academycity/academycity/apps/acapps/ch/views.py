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
    print("66-0")
    log_debug("ch home : 60-0")
    wsc = WebSiteCompany(request, web_company_id=22)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id
    log_debug("ch home : 60-00: company_obj_id_: "+str(company_obj_id_))
    print("ch home : 60-00: company_obj_id_: "+str(company_obj_id_))
    app_name = "login"
    return app_id(request, app_name, company_obj_id_)


def app_id(request, app_name, company_obj_id):
    print("66-01-09", app_name)
    log_debug("ch home : 60-03: "+app_name)
    default_branch = -1
    try:
        if request.user.is_anonymous:
            user_id = -1
            app_name = "login"
            print("not login")
        else:
            print("AAAAA")
            user_id = request.user.id
            user_ = request.user
            default_branch = user_.members.branch.id
            # print(default_branch)

            if request.user.groups.filter(name="c_admin").exists():
                app_name = "admin"

            # if request.user.groups.filter(name="t_reports_manager").exists():
            #     app_name = "reports"

            # elif request.user.groups.filter(name="t_admin").exists():
            #     if app_name == "admin":
            #         app_name = "tadmin"

            elif request.user.groups.filter(name="admins").exists():
                if app_name == "login":
                    app_name = "default"
                # app_name = "admin"
                log_debug("ch home : 60-04: "+app_name)
                # print("ch home : 60-04: "+app_name)
                pass
            else:
                app_name = "default"
            # print("ch home : 60-05: "+app_name)

    except Exception as ex:
        print(ex)
    # print("66-015", app_name, user_id)
    company_obj_id_ = company_obj_id
    app_ = "ch"
    log_debug("app_id 60-05: app_name=" + app_name + ", app_="  + app_ + ", company_obj_id_= " + str(company_obj_id_))
    # print("app_id 60-05: app_name=" + app_name + ", app_="  + app_ + ", company_obj_id_= " + str(company_obj_id_))

    app_activate_function_link_ = reverse(app_+':activate_obj_function', kwargs={})
    logmein_link_ = reverse(app_+':logmein', kwargs={})
    # log_debug("app_activate_function_link_=" + app_activate_function_link_)
    # log_debug("logmein_link_=" + logmein_link_)
    return render(request, app_+'//home.html', {"atm_name": app_+"_"+app_name+"_atm",
                                                "app": app_,
                                                "logmein_link":logmein_link_,
                                                "app_activate_function_link": app_activate_function_link_,
                                                "company_obj_id": company_obj_id_, "user_id":user_id,
                                                "default_entity":default_branch, "entity_name": "branch",
                                                "title": app_}
                  )


def appt(request, app_name):
    log_debug("ch appt: 60-03: "+app_name)
    print("ch appt: 60-03: "+app_name)
    wsc = WebSiteCompany(request, web_company_id=22, is_test=True)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id
    return app_id(request, app_name, company_obj_id_)


def app(request, app_name):
    log_debug("ch app: 60-02: "+app_name)
    print("ch app: 60-02: "+app_name)
    wsc = WebSiteCompany(request, web_company_id=22)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id
    return app_id(request, app_name, company_obj_id_)
