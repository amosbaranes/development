from django.shortcuts import render
from ...webcompanies.WebCompanies import WebSiteCompany
from ...core.utils import log_debug
from django.urls import reverse
from ...core.apps_general_functions import activate_obj_function
from django.http import HttpResponse
import os
import json


def home(request):
    app_name = "default"
    return app_id(request, app_name, -1)


def app_id(request, app_name, company_obj_id):
    log_debug("training home : 60-03: "+app_name)
    try:
        if request.user.is_anonymous:
            user_id = -1
        else:
            user_id = request.user.id
    except Exception as ex:
        print(ex)
    company_obj_id_ = company_obj_id
    app_ = "mm"
    log_debug("app_id 60-05: app_name=" + app_name + ", app_="  + app_ + ", company_obj_id_= " + str(company_obj_id_))
    app_activate_function_link_ = reverse(app_+':activate_obj_function', kwargs={})
    logmein_link_ = reverse(app_+':logmein', kwargs={})
    return render(request, app_+'//home.html', {"atm_name": app_+"_"+app_name+"_atm",
                                                "app": app_,
                                                "logmein_link":logmein_link_,
                                                "app_activate_function_link": app_activate_function_link_,
                                                "company_obj_id": company_obj_id_,
                                                "user_id":user_id,
                                                "title": app_}
                  )

def app(request, app_name):
    return app_id(request, app_name, -1)


