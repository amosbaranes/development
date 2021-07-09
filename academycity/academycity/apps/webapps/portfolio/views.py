from django.shortcuts import render
from ...webcompanies.WebCompanies import WebSiteCompany
from .models import PortfolioWeb


def home(request):
    wsc = WebSiteCompany(request, web_company_id=9)
    company_obj = wsc.site_company()
    services = wsc.site_company('services')
    projects = wsc.site_company('projects')
    return render(request, 'portfolio/home.html', {'company_obj': company_obj,
                                                   'services': services,
                                                   'projects': projects,
                                                   })


def resume(request, pk):
    wsc = WebSiteCompany(request, web_company_id=9)
    company_obj = wsc.site_company()
    return render(request, 'portfolio/resume.html',
                  {'company_obj': company_obj})
