from django.shortcuts import render
from ...webcompanies.WebCompanies import WebSiteCompany
from ...core.utils import log_debug
from django.urls import reverse
from ...core.apps_general_functions import activate_obj_function
from .models import AcMathWeb


def home(request):
    wsc = WebSiteCompany(request, web_company_id=16, is_test=True)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id
    app_ = "acmath"
    activate_obj_function_link_ = reverse(app_+':activate_obj_function', kwargs={})
    return render(request, app_+'/home.html', {"atm_name": "acmathatm", "app": app_,
                                               "app_activate_function_link": activate_obj_function_link_,
                                               "company_obj_id": company_obj_id_, "title": "AC Math"}
                  )


def app_id(request, app_name, company_obj_id):
    company_obj = AcMathWeb.objects.get_or_create(id=company_obj_id)
    app_ = "acmath"
    app_activate_function_link_ = reverse(app_+':activate_obj_function', kwargs={})
    return render(request, app_+'/home.html', {"atm_name": "acmath_"+app_name+"_tm", "app": app_,
                                               "app_activate_function_link": app_activate_function_link_,
                                               "company_obj_id": company_obj_id, "title": "AC Math"}
                  )


def app(request, app_name):
    wsc = WebSiteCompany(request, web_company_id=16, is_test=True)
    return app_id(request, app_name, wsc.site_company().id)

