from django.shortcuts import render
from ...webcompanies.WebCompanies import WebSiteCompany


def home(request):
    wsc = WebSiteCompany(request, web_company_id=1)
    company_obj = wsc.site_company()
    return render(request, 'radiusfood/home.html', {'company_obj': company_obj})


def test(request, pk):
    wsc = WebSiteCompany(request, web_company_id=pk)
    company_obj = wsc.site_company(model='', web_company_id=pk)
    return render(request, 'radiusfood/home.html', {'company_obj': company_obj})


def suppliers_registration(request):
    return render(request, 'radiusfood/suppliers_registration.html', {})

