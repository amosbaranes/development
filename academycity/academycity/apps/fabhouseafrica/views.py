from django.shortcuts import render
from .models import FabHoseAfricaWeb, Home, CatalogSectionCategory, Contact
from django.core.mail import EmailMessage
from .models import ReceivedMessages
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..webcompanies.WebCompanies import WebSiteCompany
from ..webcompanies.models import WebCompanies


def home(request):
    wsc = WebSiteCompany(request)
    if wsc.is_registered_domain():
        web_company_id = wsc.web_site_company['web_company_id']
        web_company = WebCompanies.objects.get(id=web_company_id)
    else:
        web_company = WebCompanies.objects.get(id=1)

    company = web_company.target
    home_obj = company.home
    return render(request, 'fabhouseafrica/home.html', {'company_obj': company, 'home_obj': home_obj})


def catalog(request):
    web_company = WebCompanies.objects.get(id=1)
    fab = web_company.target
    catalog_obj = fab.catalog
    return render(request, 'fabhouseafrica/catalog.html', {'company_obj': fab, 'catalog_obj': catalog_obj})


def category(request, category_id):
    web_company = WebCompanies.objects.get(id=1)
    fab = web_company.target
    catalog_obj = fab.catalog
    category_obj = CatalogSectionCategory.objects.get(id=category_id)
    section_obj = category_obj.section
    return render(request, 'fabhouseafrica/style.html', {'category_obj': category_obj, 'section_obj': section_obj,
                                                         'company_obj': fab, 'catalog_obj': catalog_obj})


def about(request):
    web_company = WebCompanies.objects.get(id=1)
    fab = web_company.target
    about_obj = fab.about
    return render(request, 'fabhouseafrica/about.html', {'company_obj': fab, 'about_obj': about_obj})


def contact(request):
    web_company = WebCompanies.objects.get(id=1)
    fab = web_company.target
    contact_obj = fab.contact
    return render(request, 'fabhouseafrica/contact.html', {'company_obj': fab, 'contact_obj': contact_obj})


def post_contact_us(request):
    contact_id = request.POST.get('contact_id')
    contact_us_name = request.POST.get('contact_us_name')
    contact_us_email = request.POST.get('contact_us_email')
    print(contact_us_email)
    contact_us_subject = request.POST.get('contact_us_subject')
    contact_us_message = request.POST.get('contact_us_message')
    if contact_us_subject == '' or contact_us_message == '':
        rr = {'status': 'Must enter subject and a message!'}
    else:
        rr = {'status': 'got it'}
        contact_us_message = 'Received email from: ' + contact_us_email + '\n\n' + request.POST.get('contact_us_message')
        try:
            contact_ = Contact.objects.get(id=contact_id)
            email = EmailMessage(contact_us_subject, contact_us_message, contact_us_email, [contact_.contact_us_email])
            email.send()
            ReceivedMessages.objects.create(contact=contact_, name=contact_us_name, email=contact_us_email,
                                            subject=contact_us_subject, message=contact_us_message)
            rr = {'status': 'Your message was received.\n\nThank you.'}
        except Exception as ee:
            rr = {'status': 'ko'}
    return JsonResponse(rr)


def gallery(request):
    web_company = WebCompanies.objects.get(id=1)
    fab = web_company.target
    gallery_obj = fab.gallery
    page = request.GET.get('page', 1)
    print(page)
    paginator = Paginator(gallery_obj.gallery_items.all(), 12)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, 'fabhouseafrica/gallery.html', {
        'company_obj': fab, 'gallery_obj': gallery_obj
        , 'item_images': items
    })
