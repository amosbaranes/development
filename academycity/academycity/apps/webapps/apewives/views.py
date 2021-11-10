from django.shortcuts import render
from django.core.mail import EmailMessage
from django.http import JsonResponse
from ...webcompanies.WebCompanies import WebSiteCompany


def home(request):
    wsc = WebSiteCompany(request, web_company_id=11)
    company_obj = wsc.site_company()
    return render(request, 'apewives/home.html', {'company_obj': company_obj})
