from django.shortcuts import render
from ...webcompanies.WebCompanies import WebSiteCompany
from ...core.utils import log_debug
from django.urls import reverse
from ...core.apps_general_functions import activate_obj_function
from django.http import HttpResponse
# from .objects import DataProcessing
import os
import json


def home(request):
    app_name = "default"
    return app_id(request, app_name, -1)


def app_id(request, app_name, company_obj_id):
    company_obj_id_ = company_obj_id
    app_ = "avib"
    app_activate_function_link_ = reverse(app_+':activate_obj_function', kwargs={})
    return render(request, app_+'//home.html', {"atm_name": app_+"_"+app_name+"_atm",
                                                "app": app_,
                                                "app_activate_function_link": app_activate_function_link_,
                                                "company_obj_id": company_obj_id_,
                                                "title": app_}
                  )


def app(request, app_name):
    return app_id(request, app_name, -1)

