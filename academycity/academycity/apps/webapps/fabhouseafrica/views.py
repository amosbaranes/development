from django.shortcuts import render
from .models import FabHoseAfricaWeb, Home, CatalogSectionCategory, Contact
from django.core.mail import EmailMessage
from .models import ReceivedMessages
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ...webcompanies.WebCompanies import WebSiteCompany


def home(request):
    wsc = WebSiteCompany(request, web_company_id=1, is_test=True)
    company_obj = wsc.site_company()
    home_obj = company_obj.home
    return render(request, 'fabhouseafrica/home.html', {'company_obj': company_obj, 'home_obj': home_obj})


def test(request, pk):
    wsc = WebSiteCompany(request, web_company_id=pk)
    company_obj = wsc.site_company(model='', web_company_id=pk)
    home_obj = company_obj.home
    return render(request, 'fabhouseafrica/home.html', {'company_obj': company_obj, 'home_obj': home_obj})


def catalog(request):
    wsc = WebSiteCompany(request, web_company_id=1)
    company_obj = wsc.site_company()
    catalog_obj = company_obj.catalog
    return render(request, 'fabhouseafrica/catalog.html', {'company_obj': company_obj, 'catalog_obj': catalog_obj})


def category(request, category_id):
    wsc = WebSiteCompany(request, web_company_id=1)
    company_obj = wsc.site_company()
    catalog_obj = company_obj.catalog
    category_obj = CatalogSectionCategory.objects.get(id=category_id)
    section_obj = category_obj.section
    return render(request, 'fabhouseafrica/style.html', {'category_obj': category_obj, 'section_obj': section_obj,
                                                         'company_obj': company_obj, 'catalog_obj': catalog_obj})


def about(request):
    wsc = WebSiteCompany(request, web_company_id=1)
    company_obj = wsc.site_company()
    about_obj = company_obj.about
    return render(request, 'fabhouseafrica/about.html', {'company_obj': company_obj, 'about_obj': about_obj})


def contact(request):
    wsc = WebSiteCompany(request, web_company_id=1)
    company_obj = wsc.site_company()
    contact_obj = company_obj.contact
    return render(request, 'fabhouseafrica/contact.html', {'company_obj': company_obj, 'contact_obj': contact_obj})


def post_contact_us(request):
    contact_id = request.POST.get('contact_id')
    contact_us_name = request.POST.get('contact_us_name')
    contact_us_email = request.POST.get('contact_us_email')
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
    wsc = WebSiteCompany(request, web_company_id=1)
    company_obj = wsc.site_company()
    gallery_obj = company_obj.gallery
    page = request.GET.get('page', 1)
    paginator = Paginator(gallery_obj.gallery_items.all(), 12)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, 'fabhouseafrica/gallery.html', {
        'company_obj': company_obj, 'gallery_obj': gallery_obj
        , 'item_images': items
    })
