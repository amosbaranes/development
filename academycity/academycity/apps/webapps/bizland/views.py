from django.shortcuts import render
from .models import BizlandWeb, Contact, ReceivedMessages
from django.core.mail import EmailMessage
from django.http import JsonResponse
from ...webcompanies.WebCompanies import WebSiteCompany
from .models import PortfolioItem


def home(request):
    wsc = WebSiteCompany(request, web_company_id=2)
    company_obj = wsc.site_company()
    return render(request, 'bizland/home.html', {'company_obj': company_obj})


def test(request, pk):
    wsc = WebSiteCompany(request, web_company_id=pk)
    company_obj = wsc.site_company(model='', web_company_id=pk)
    return render(request, 'portfolio/home.html', {'company_obj': company_obj})


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


def category_items(request):
    category_id_ = request.POST.get('category_id')
    # print(category_id_)
    # print('-2'*50)
    items_ = PortfolioItem.objects.filter(portfolio_category__id=category_id_).values()
    # items_ = [entry for entry in items_]
    items = {}
    for t in items_:
        items[t['id']] = t
    # print(items)

    return JsonResponse(items)
