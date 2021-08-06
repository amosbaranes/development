from django.shortcuts import render
from ...webcompanies.WebCompanies import WebSiteCompany
from .models import PortfolioWeb, Service


def home(request):
    wsc = WebSiteCompany(request, web_company_id=9)
    company_obj = wsc.site_company()
    services = wsc.site_company('services')
    projects = wsc.site_company('projects')
    return render(request, 'portfolio/home.html', {'company_obj': company_obj,
                                                   'services': services,
                                                   'projects': projects,
                                                   })


def test(request, pk):
    wsc = WebSiteCompany(request, web_company_id=pk)
    company_obj = wsc.site_company(model='', web_company_id=pk)
    services = wsc.site_company(model='services', web_company_id=pk)
    projects = wsc.site_company(model='projects', web_company_id=pk)
    return render(request, 'portfolio/home.html', {'company_obj': company_obj,
                                                   'services': services,
                                                   'projects': projects,
                                                   })


def resume(request, pk):
    company_obj = PortfolioWeb.objects.get(id=pk)
    return render(request, 'portfolio/resume.html',
                  {'company_obj': company_obj})


def service(request, pk):
    company_obj = PortfolioWeb.objects.get(id=pk)
    services = Service.objects.all()
    return render(request, 'portfolio/service.html',
                  {'company_obj': company_obj, 'services': services})
