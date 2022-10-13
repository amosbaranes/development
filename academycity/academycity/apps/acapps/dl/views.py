from django.shortcuts import render
from ...webcompanies.WebCompanies import WebSiteCompany
from ...core.utils import log_debug
from django.urls import reverse
from ...core.apps_general_functions import activate_obj_function
from .models import DLWeb


def home(request):
    wsc = WebSiteCompany(request, web_company_id=18, is_test=True)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id
    app_ = "dl"
    activate_obj_function_link_ = reverse(app_+':activate_obj_function', kwargs={})
    return render(request, app_+'/home.html', {"atm_name": "dl_default_tm", "app": app_,
                                               "app_activate_function_link": activate_obj_function_link_,
                                               "company_obj_id": company_obj_id_, "title": "Deep Learning"}
                  )


def app_id(request, app_name, company_obj_id):
    company_obj = DLWeb.objects.get_or_create(id=company_obj_id)
    app_ = "dl"
    app_activate_function_link_ = reverse(app_+':activate_obj_function', kwargs={})
    return render(request, app_+'/home.html', {"atm_name": "dl_"+app_name+"_tm", "app": app_,
                                               "app_activate_function_link": app_activate_function_link_,
                                               "company_obj_id": company_obj_id, "title": "Deep Learning"}
                  )


def app(request, app_name):
    wsc = WebSiteCompany(request, web_company_id=18, is_test=True)
    return app_id(request, app_name, wsc.site_company().id)

