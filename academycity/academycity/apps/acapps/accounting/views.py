from django.shortcuts import render
from ...webcompanies.WebCompanies import WebSiteCompany


def home(request):
    wsc = WebSiteCompany(request, web_company_id=12)
    company_obj = wsc.site_company()
    # print(company_obj)
    company_obj_id_ = company_obj.id
    return render(request, 'accounting/home.html', {"atm_name": "aatm", "app": "accounting",
                                                    "company_obj_id": company_obj_id_, "title": "Accounting"}
                  )

