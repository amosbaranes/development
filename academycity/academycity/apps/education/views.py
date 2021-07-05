from django.shortcuts import render
from ..webcompanies.models import WebCompanies
from django.core.mail import EmailMessage
from django.http import JsonResponse
from ..webcompanies.WebCompanies import WebSiteCompany
from django.http import JsonResponse
from .models import Phrase, AdditionalTopic


def institution(request, model=''):
    try:
        wsc = WebSiteCompany(request)
        if wsc.is_registered_domain():
            web_company_id = wsc.web_site_company['web_company_id']
            web_company = WebCompanies.objects.get(id=web_company_id)
        else:
            web_company = WebCompanies.objects.get(id=7)
    except Exception as ex:
        print(ex)

    if model != '':
        s = "objs = web_company.target."+model+".all()"
        dic_ = {'web_company': web_company}
        exec(s, dic_)
        objs = dic_['objs']
    else:
        objs = web_company.target
    return objs


def home(request):
    institution_ = institution(request)
    phrases_ = Phrase.objects.all()
    topics_ = AdditionalTopic.objects.all()
    return render(request, 'education/home.html', {'institution_obj': institution_,
                                                   'phrases': phrases_,
                                                   'topics': topics_
                                                   })


def get_courses(request):
    courses = institution(request, 'courses')
    rr = {}
    for course in courses:
        rr[str(course.id)] = {
                                'course_name': course.course_name,
                                'order': course.order,
                                'course_description': course.course_description,
                                'course_date': course.course_date,
                                'is_popular': course.is_popular,
                                'image_url': course.image.url
                                }
    return JsonResponse(rr)


def get_news(request):
    news = institution(request, 'news')
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

    programs = institution(request, 'programs')

    rr = {}
    for program in programs:
        print('-' * 50)
        rr[str(program.id)] = {
            'program_title': program.program_title,
            'order': program.order,
            'program_description': program.program_description,
            'is_popular': program.is_popular,
            'image_url': program.image.url
        }
    return JsonResponse(rr)


def get_subject(request):

    subjects = institution(request, 'subjects')

    rr = {}
    for subject in subjects:
        print('-' * 50)
        rr[str(subject.id)] = {
            'subject_name': subject.subject_name,
            'order': subject.order,
            'is_popular': subject.is_popular,
            'image_url': subject.image.url
        }
    return JsonResponse(rr)


def get_person(request):

    persons = institution(request, 'persons')

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
