from django.shortcuts import render


def home(request):
    wsc = WebSiteCompany(request, web_company_id=13)
    company_obj = wsc.site_company()
    print(company_obj)
    company_obj_id_ = company_obj.id
    return render(request, 'macroeconomics/home.html', {"atm_name": "matm", "app": "businesssim",
                                                        "company_obj_id": company_obj_id_, "title": "Macro Economics"}
    )
