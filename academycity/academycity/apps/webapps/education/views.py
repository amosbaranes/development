from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from ...webcompanies.WebCompanies import WebSiteCompany
from django.http import JsonResponse
from .models import Phrase, AdditionalTopic, Course, Program, MoreNewsDetail, Subject, Services, New
from django.urls import reverse


def home(request):
    wsc = WebSiteCompany(request, web_company_id=7)
    company_obj = wsc.site_company()
    phrases_ = wsc.site_company('phrases')
    topics_ = wsc.site_company('topics')
    courses = wsc.site_company('courses')
    programs = wsc.site_company('programs')
    services = wsc.site_company('services')
    news = wsc.site_company('news')
    persons = wsc.site_company('persons')
    subjects = wsc.site_company('subjects')
    return render(request, 'education/home.html', {'institution_obj': company_obj,
                                                   'phrases': phrases_,
                                                   'topics': topics_,
                                                   'courses': courses,
                                                   'programs': programs,
                                                   'services': services,
                                                   'news': news,
                                                   'persons': persons,
                                                   'subjects': subjects
                                                   })


def course_description(request, pk):
    wsc = WebSiteCompany(request, web_company_id=7)
    company_obj = wsc.site_company()
    course = Course.objects.get(id=pk)
    return render(request, 'education/course_description.html',
                  {'course': course,
                   'institution_obj': company_obj,
                   })


def program_description(request, pk):
    wsc = WebSiteCompany(request, web_company_id=7)
    company_obj = wsc.site_company()
    program = Program.objects.get(id=pk)
    return render(request, 'education/program_description.html',
                  {'program': program,
                   'institution_obj': company_obj,
                   })


def subject_description(request, pk):
    wsc = WebSiteCompany(request, web_company_id=7)
    company_obj = wsc.site_company()
    subject = Subject.objects.get(id=pk)
    return render(request, 'education/subject_description.html',
                  {'subject': subject,
                   'institution_obj': company_obj,
                   })


def news_detail(request):
    wsc = WebSiteCompany(request, web_company_id=7)
    company_obj = wsc.site_company()
    news_detail_ = MoreNewsDetail.objects.all()
    return render(request, 'education/news_detail.html', {'news_detail_': news_detail_,
                                                          'institution_obj': company_obj,
                                                          })


def service_description(request, pk):
    wsc = WebSiteCompany(request, web_company_id=7)
    company_obj = wsc.site_company()
    service = Services.objects.get(id=pk)
    return render(request, 'education/service_description.html',
                  {'service': service,
                   'institution_obj': company_obj,
                   })


def additional_topics(request, pk):
    wsc = WebSiteCompany(request, web_company_id=7)
    company_obj = wsc.site_company()

    is_admin = request.user.groups.filter(name='admins').exists()
    if is_admin:
        topics = AdditionalTopic.objects.all()
        for obj in topics:
            obj.save()

    topics = AdditionalTopic.objects.get(id=pk)
    return render(request, 'education/additional_topics.html',
                  {'topics': topics,
                   'institution_obj': company_obj,
                   })


def news_description(request, pk):
    wsc = WebSiteCompany(request, web_company_id=7)
    company_obj = wsc.site_company()
    news = New.objects.get(id=pk)
    return render(request, 'education/news_description.html',
                  {'news': news,
                   'institution_obj': company_obj,
                   })




