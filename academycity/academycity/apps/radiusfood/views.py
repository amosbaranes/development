from django.shortcuts import render
from ..webcompanies.models import WebCompanies
from ..webcompanies.WebCompanies import WebSiteCompany


def home(request):

    wsc = WebSiteCompany(request)
    if wsc.is_registered_domain():
        web_company_id = wsc.web_site_company['web_company_id']
        web_company = WebCompanies.objects.get(id=web_company_id)
    else:
        web_company = WebCompanies.objects.get(id=3)

    company = web_company.target
    return render(request, 'radiusfood/home.html', {'company_obj': company})


def suppliers_registration(request):
    return render(request, 'radiusfood/suppliers_registration.html', {})

