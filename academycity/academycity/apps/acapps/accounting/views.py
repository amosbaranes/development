from django.shortcuts import render
from ...webcompanies.WebCompanies import WebSiteCompany
from ...core.utils import log_debug
from django.urls import reverse
from ...core.apps_general_functions import activate_obj_function


def home(request):
    wsc = WebSiteCompany(request, web_company_id=12, is_test=True)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id
    app_ = "accounting"
    app_activate_function_link_ = reverse(app_+':activate_obj_function', kwargs={})
    return render(request, 'accounting/home.html', {"atm_name": "aatm",
                                                    "app": app_,
                                                    "app_activate_function_link": app_activate_function_link_,
                                                    "company_obj_id": company_obj_id_,
                                                    "title": "Accounting"}
                  )


def app(request, app_name):
    wsc = WebSiteCompany(request, web_company_id=12, is_test=True)
    company_obj = wsc.site_company()
    company_obj_id_ = company_obj.id
    app_ = "accounting"
    app_activate_function_link_ = reverse(app_+':activate_obj_function', kwargs={})
    return render(request, 'accounting/home.html', {"atm_name": "co_"+app_name+"_tm",
                                                               "app": app_,
                                                               "app_activate_function_link": app_activate_function_link_,
                                                               "company_obj_id": company_obj_id_,
                                                               "title": "Accounting"}
                  )

