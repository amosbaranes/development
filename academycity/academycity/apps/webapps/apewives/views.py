from django.shortcuts import render
from django.core.mail import EmailMessage
from django.http import JsonResponse
from ...webcompanies.WebCompanies import WebSiteCompany
from ...core.utils import log_debug, clear_log_debug


def home(request):
    # clear_log_debug()
    wsc = WebSiteCompany(request, web_company_id=11, is_test=True)
    company_obj = wsc.site_company()
    return render(request, 'apewives/home.html', {'company_obj': company_obj})
