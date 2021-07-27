from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from ...webcompanies.WebCompanies import WebSiteCompany
from django.http import JsonResponse
from .models import Phrase, AdditionalTopic, Course, Program, MoreNewsDetail, Subject, Services
from django.urls import reverse


def home(request):
    wsc = WebSiteCompany(request, web_company_id=7)
    company_obj = wsc.site_company()
    phrases_ = wsc.site_company('phrases')
    topics_ = wsc.site_company('topics')

    return render(request, 'education/home.html', {'institution_obj': company_obj,
                                                   'phrases': phrases_,
                                                   'topics': topics_
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


def get_courses(request):
    wsc = WebSiteCompany(request, web_company_id=7)
    courses = wsc.site_company('courses')
    is_admin = request.user.groups.filter(name='admins').exists()
    if is_admin:
        for obj in courses:
            obj.save()
    rr = {}
    for course in courses:
        rr[str(course.id)] = {
                                'name': course.name,
                                'order': course.order,
                                'date': course.date,
                                'is_popular': course.is_popular,
                                'image_url': course.image.url,
                                'short_description': course.short_description
                                }

    return JsonResponse(rr)


def get_news(request):
    wsc = WebSiteCompany(request, web_company_id=7)
    news = wsc.site_company('news')
    rr = {}
    for new in news:
        if new.is_active:
            rr[str(new.id)] = {
                'news_title': new.news_title,
                'news_type': new.news_type,
                'order': new.order,
                'news_description': new.news_description,
                'news_type_description': new.news_type_description,
                'news_date': new.news_date,
                'is_popular': new.is_popular,
                'image_url': new.image.url
            }
    return JsonResponse(rr)


def get_program(request):
    wsc = WebSiteCompany(request, web_company_id=7)
    programs = wsc.site_company('programs')
    is_admin = request.user.groups.filter(name='admins').exists()
    if is_admin:
        for obj in programs:
            obj.save()
    rr = {}
    for program in programs:
        print('-' * 50)
        rr[str(program.id)] = {
            'name': program.name,
            'order': program.order,
            'short_description': program.short_description,
            'is_popular': program.is_popular,
            'image_url': program.image.url
        }
    return JsonResponse(rr)


def get_subject(request):
    wsc = WebSiteCompany(request, web_company_id=7)
    subjects = wsc.site_company('subjects')
    rr = {}
    for subject in subjects:
        print('-' * 50)
        rr[str(subject.id)] = {
            'name': subject.name,
            'order': subject.order,
            'is_popular': subject.is_popular,
            'image_url': subject.image.url
        }
    return JsonResponse(rr)


def get_person(request):
    wsc = WebSiteCompany(request, web_company_id=7)
    persons = wsc.site_company('persons')
    rr = {}
    for person in persons:
        print('-' * 50)
        rr[str(person.id)] = {
            'persons_name': person.persons_name,
            'persons_duty': person.persons_duty,
            'persons_description': person.persons_description,
            'order': person.order,
            'is_popular': person.is_popular,
            'image_url': person.image.url
        }
    return JsonResponse(rr)


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


def get_service(request):
    wsc = WebSiteCompany(request, web_company_id=7)
    services = wsc.site_company('services')
    is_admin = request.user.groups.filter(name='admins').exists()
    if is_admin:
        for obj in services:
            obj.save()
    rr = {}
    for service in services:
        rr[str(service.id)] = {
            'name': service.name,
            'order': service.order,
            'short_description': service.short_description,
            'image_url': service.image.url
        }
    return JsonResponse(rr)


def noa(request):
    return render(request, 'education/Noa.html', {})
