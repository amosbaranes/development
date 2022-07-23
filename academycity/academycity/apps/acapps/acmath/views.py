from django.shortcuts import render
from ...webcompanies.WebCompanies import WebSiteCompany
from ...core.utils import log_debug


def home(request):
    log_debug("acmath_0")
    wsc = WebSiteCompany(request, web_company_id=16, is_test=True)
    log_debug("acmath_1")
    company_obj = wsc.site_company()
    log_debug("acmath_2")
    company_obj_id_ = company_obj.id
    log_debug(company_obj_id_)
    log_debug("acmath_3")
    return render(request, 'accounting/home.html', {"atm_name": "acmathatm", "app": "acmath",
                                                    "company_obj_id": company_obj_id_, "title": "AC Math"}
                  )
