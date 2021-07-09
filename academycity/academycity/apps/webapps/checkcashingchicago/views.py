from django.shortcuts import render
from django.core.mail import EmailMessage
from django.http import JsonResponse
from ...webcompanies.WebCompanies import WebSiteCompany
from django.http import JsonResponse
from .models import CheckCashingWeb
from .models import Currency, Partner, Location, ContactUsMessages
from django.urls import reverse
from django.shortcuts import redirect


def home(request):
    wsc = WebSiteCompany(request, web_company_id=8)
    company_obj = wsc.site_company()
    locations = wsc.site_company('locations')
    currencies = Currency.objects.all()
    partners = Partner.objects.all()
    return render(request, 'checkcashingchicago/home.html', {'company_obj': company_obj,
                                                             'currencies': currencies,
                                                             'locations': locations,
                                                             'partners': partners,
                                                             })


def location_detail(request, slug):
    wsc = WebSiteCompany(request, web_company_id=8)
    company_obj = wsc.site_company()
    partners = Partner.objects.all()
    location = Location.objects.get(slug=slug)

    l_all = Location.objects.filter(check_cashing_web=company_obj).all()
    l_first = l_all[0]
    l_last = l_all[len(l_all)-1]

    next_l = None
    prev_l = None

    if l_first.id == location.id:
        next_l = (Location.objects.filter(id__gt=location.id).exclude(id=location.id).order_by('id').first())
    elif l_last.id == location.id:
        prev_l = (Location.objects.filter(id__lt=location.id).exclude(id=location.id).order_by('id').first())
    else:
        next_l = (Location.objects.filter(id__gt=location.id).exclude(id=location.id).order_by('id').first())
        prev_l = (Location.objects.filter(id__lt=location.id).exclude(id=location.id).order_by('id').first())

    return render(request, 'checkcashingchicago/location_detail.html', {'location': location,
                                                                        'company_obj': company_obj,
                                                                        'partners': partners,
                                                                        'prev_l': prev_l,
                                                                        'next_l': next_l
                                                                        })


def members_area_detail(request):
    wsc = WebSiteCompany(request, web_company_id=8)
    company_obj = wsc.site_company()
    partners = Partner.objects.all()
    return render(request, 'checkcashingchicago/members_area_detail.html', {'company_obj': company_obj,
                                                                            'partners': partners,
                                                                            })


def post_password(request):
    wsc = WebSiteCompany(request, web_company_id=8)
    company_obj = wsc.site_company()
    pass_word_ = request.POST.get('pass_word')
    members_password_ = company_obj.members_password

    if pass_word_ != members_password_:
        print('ko')
        rr = {'status': 'Wrong Password!'}
        return JsonResponse(rr)

    return render(request, 'checkcashingchicago/members_area_doc.html', {'company_obj': company_obj})


# not used we should delete it
def get_location(request):
    # locations = check_cashing(request, 'locations')
    rr = {}
    # print(locations)
    # for location in locations:
    #     print(location.image)
    #     rr[str(location.id)] = {
    #                             'location_heading': location.location_heading,
    #                             'order': location.order,
    #                             'image_url': location.image.url,
    #                             'location_info': location.location_info,
    #                             'data_ajax_id': location.data_ajax_id,
    #                             'grid_loop': location.grid_loop,
    #                             'grid_parity': location.grid_parity,
    #                             'south_suburbs_sort': location.south_suburbs_sort
    #                             }

    return JsonResponse(rr)


def post_contact_us(request):
    company_id_ = request.POST.get('company_id')
    contact_us_name = request.POST.get('contact_us_name')
    contact_us_email = request.POST.get('contact_us_email')
    contact_us_message = request.POST.get('contact_us_message')
    if contact_us_message == '':
        rr = {'status': 'a message!'}
    else:
        rr = {'status': 'got it'}
        try:
            company_ = CheckCashingWeb.objects.get(id=company_id_)
            email = EmailMessage("Email received from contact us.", contact_us_message, contact_us_email, [company_.contact_us_email])
            email.send()
            ContactUsMessages.objects.create(check_cashing_web=company_, name=contact_us_name, email=contact_us_email,
                                             message=contact_us_message)
            rr = {'status': 'Your message was received.\n\nThank you.'}
        except Exception as ee:
            rr = {'status': 'Error sending your massage'}
    return JsonResponse(rr)

