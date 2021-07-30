from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404
from .models import (Countries, Towns, ReceivedMessages, Projects, Directors, Services, NewAnnouncements, Tenders, Tourism,
                     Careers, Conferencing)
from django.http import JsonResponse
from django.apps import apps
from django.core.mail import EmailMessage
from allauth.account.forms import LoginForm, SignupForm
from django.urls import reverse
from ..webcompanies.models import WebCompanies
from ..webcompanies.WebCompanies import WebSiteCompany


def index(request, town_slug=None):
    # print(22333333)
    if town_slug:
        town_ = get_object_or_404(Towns, slug=town_slug)
    else:
        # print('--- rrr ---')
        wsc = WebSiteCompany(request, web_company_id=4)
        country_id = wsc.get("country_id")
        town_ = Towns.objects.filter(country__id=country_id).all()[0]
    return menu_town__(request, town_, item_=None)


# Need to remove this function
# was replaced by home function
def ut_login_page(request):
    # print('ut_login_page')
    # print(ut_login_page)
    # print('ut_login_page')

    wsc = WebSiteCompany(request)
    if wsc.is_registered_domain():
        web_company_id = wsc.web_site_company['web_company_id']
        web_company = WebCompanies.objects.get(id=web_company_id)
    else:
        web_company = WebCompanies.objects.get(id=4)
    country = web_company.target
    wsc.add('country_id', country.id)

    # print('ut_login_page   wsc.web_site_company')
    # print(wsc.web_site_company)
    # print('ut_login_page   wsc.web_site_company')

    country = Countries.objects.get(id=country.id)

    form_class = LoginForm
    form_signup = SignupForm
    return render(request, 'ugandatowns/login_page.html', {
        'company_obj': country,
        'form': form_class,
        'form_signup': form_signup,
        'redirect_field_name': 'next',
        'redirect_field_value': reverse('ugandatowns:index')})


def home(request):
    # print('u h')
    wsc = WebSiteCompany(request, web_company_id=4)
    if wsc.is_registered_domain():
        web_company_id = wsc.web_site_company['web_company_id']
        web_company = WebCompanies.objects.get(id=web_company_id)
    else:
        web_company = WebCompanies.objects.get(id=4)
    country = web_company.target
    wsc.add(request, 'country_id', country.id)

    # print('home wsc.web_site_company')
    # print(wsc.web_site_company)
    # print('home wsc.web_site_company')

    country = Countries.objects.get(id=country.id)

    form_class = LoginForm
    form_signup = SignupForm
    return render(request, 'ugandatowns/login_page.html', {
        'company_obj': country,
        'form': form_class,
        'form_signup': form_signup,
        'redirect_field_name': 'next',
        'redirect_field_value': reverse('ugandatowns:index')})


def create_conference(request):
    name_ = request.POST.get('name')
    conference, created = Conferencing.objects.get_or_create(conference_name=name_, tc_user=request.user)
    conferences_ = Conferencing.objects.all()
    return render(request, 'ugandatowns/_conferences.html', {'conferences': conferences_})


def remove_conference(request):
    conference_number_ = request.POST.get('conference_number')
    conference = Conferencing.objects.get(conference_number=conference_number_)
    conference.active = False
    conference.save()

    conferences_ = Conferencing.objects.all()
    return render(request, 'ugandatowns/_conferences.html', {'conferences': conferences_})


def basic_town(request):
    slug_ = request.POST.get('slug')
    town_ = Towns.objects.get(slug=slug_)
    projects = Projects.objects.filter(town=town_, active=True).all()
    directors = Directors.objects.filter(town=town_, active=True).all()
    services = Services.objects.filter(town=town_, active=True).all()
    newannouncements = NewAnnouncements.objects.filter(town=town_, active=True).all()
    tenders = Tenders.objects.filter(town=town_, active=True).all()
    careers = Careers.objects.filter(town=town_, active=True).all()
    tourism = Tourism.objects.filter(town=town_, active=True).all()
    return render(request, 'ugandatowns/basic_town.html', {'town': town_, 'projects': projects,
                                                           'directors': directors, 'services': services,
                                                           'newannouncements': newannouncements, 'tenders': tenders,
                                                           'careers': careers, 'tourism': tourism})


def menu_town_other_model(request, town_slug=None, html=None):
    town_slug_ = town_slug
    town_ = Towns.objects.get(slug=town_slug_)
    return menu_town__(request, town_, None, html)


def menu_town_model(request, town_slug=None, menu=None, item_slug=None):
    town_slug_ = town_slug
    item_slug_ = item_slug
    town_ = Towns.objects.get(slug=town_slug_)
    menu_ = menu
    return menu_town_(request, town_, item_slug_, menu_)


def menu_town(request):
    town_slug_ = request.POST.get('town_slug')
    town_ = Towns.objects.get(slug=town_slug_)
    menu_ = request.POST.get('menu_')
    if menu_ == 'contact_us':
        return render(request, 'ugandatowns/contact_us.html', {'town': town_})
    else:
        item_slug_ = request.POST.get('item_slug')
        # menu_town_(request, town_, item_slug_, menu_)
        model_ = apps.get_model(app_label='ugandatowns', model_name=menu_)
        item_ = get_object_or_404(model_, town=town_, slug=item_slug_)
        return render(request, 'ugandatowns/basic_town_item.html', {'item': item_})


def menu_town_(request, town_, item_slug_, menu_):
    model_ = apps.get_model(app_label='ugandatowns', model_name=menu_)
    item_ = get_object_or_404(model_, town=town_, slug=item_slug_)
    return menu_town__(request, town_, item_)


def menu_town__(request, town_, item_, html_=None):
    projects = Projects.objects.filter(town=town_, active=True).all()
    directors = Directors.objects.filter(town=town_, active=True).all()
    services = Services.objects.filter(town=town_, active=True).all()
    newannouncements = NewAnnouncements.objects.filter(town=town_, active=True).all()
    tenders = Tenders.objects.filter(town=town_, active=True).all()
    careers = Careers.objects.filter(town=town_, active=True).all()
    tourism = Tourism.objects.filter(town=town_, active=True).all()
    conferences_ = Conferencing.objects.all()

    wsc = WebSiteCompany(request)
    country_id = wsc.get("country_id")
    country = Countries.objects.get(id=country_id)

    return render(request, 'ugandatowns/home.html', {'company_obj': country, 'town': town_, 'item': item_,
                                                     'projects': projects, 'directors': directors,
                                                     'services': services, 'newannouncements': newannouncements,
                                                     'tenders': tenders, 'careers': careers, 'tourism': tourism,
                                                     'html': html_, 'conferences': conferences_})


def post_contact_us(request):
    slug = request.POST.get('slug')
    contact_us_name= request.POST.get('contact_us_name')
    contact_us_email = request.POST.get('contact_us_email')
    contact_us_subject = request.POST.get('contact_us_subject')
    contact_us_message = request.POST.get('contact_us_message')
    if contact_us_subject == '' or contact_us_message == '':
        rr = {'status': 'Must enter subject and a message!'}
    else:
        rr = {'status': 'got it'}
        try:
            town_ = Towns.objects.get(slug=slug)
            email = EmailMessage(contact_us_subject, contact_us_message, contact_us_email, [town_.contact_us_email])
            email.send()
            ReceivedMessages.objects.create(town=town_, name=contact_us_name, email=contact_us_email,
                                            subject=contact_us_subject, message=contact_us_message)
            rr = {'status': 'Your message was received.\n\nThank you.'}
        except Exception as ee:
            rr = {'status': 'ko'}
    return JsonResponse(rr)


def town(request, town_id):
    # current_site = get_current_site(request)
    town_ = Towns.objects.get(slug=slug)
    return render(request, 'ugandatowns/town.html', {'town': town_})
