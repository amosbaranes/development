from django.shortcuts import render
from .models import Partners, Instructors
from taggit.models import Tag
from django.shortcuts import get_object_or_404
from django.conf import settings
from redis import StrictRedis
from django.contrib.auth.models import User
from allauth.account.forms import LoginForm, SignupForm
from django.contrib.sites.shortcuts import get_current_site
from ..core.utils import log_debug

try:
    r = StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
except Exception:
    print("redis try failed")

from django.http import HttpResponseRedirect
from django.urls import reverse
from ..webcompanies.WebCompanies import WebSiteCompany


def home(request):
    # log_debug('partners home0: ')
    host = request.META["HTTP_HOST"]
    log_debug('partners host: ' + host)
    host = host.split(':')[0]
    # log_debug('partners host1: ' + host)
    host_s = host.split('.')
    town = None
    host_ = None

    # print('host_0')
    # print(host_)
    # print('host_0')

    if len(host_s) > 2:
        host_ = host_s[1]
        town = host_s[0]
        # log_debug('partners town: ' + town)
    else:
        host_ = host_s[0]
    # log_debug('partners host_: ' + host_)

    # print('host_')
    # print(host_)
    # print('host_')

    try:
        log_debug('try1: ' + host_)
        wsc = WebSiteCompany(request, host_)
        if wsc.is_registered_domain():
            # print('wsc.is_registered_domain():wsc.is_registered_domain()')
            return wsc.get_redirect_link()
    except Exception as ex:
        log_debug('exception Partners:home error: ' + str(ex))

    # if host_ == "ugandatowns":
    #     if town:
    #         return HttpResponseRedirect(reverse('ugandatowns:town', kwargs={'town': town}))
    #     return HttpResponseRedirect(reverse('ugandatowns:ut_login_page'))

    user_counter = 100
    try:
        user_counter = r.incr('user:{}:views'.format(request.user.id))
        # print('='*100)
        # print(request.user.id, user_counter)
        # print('='*100)
        # r.zincrby('user_ranking', request.user.id, 2)
    except Exception as ex:
        pass
        # print("e0-"*50)
        # print(ex)
        # print("e1-"*50)
    partners = Partners.objects.all().order_by('order')
    # user_ranking = ranking()

    form_class = LoginForm
    form_signup = SignupForm
    redirect_field_name = "next"
    current_site = get_current_site(request)

    home_test = 'hometest'
    return render(request, 'partners/home.html', {'host': host, 'host_': host_, 'town': town,
                                                  'current_site': current_site,
        'partners': partners,
        'user_counter': user_counter,
        'form' : form_class,
        'form_signup': form_signup,
        'redirect_field_name': redirect_field_name
        # ,
        # 'user_ranking': user_ranking
    })


# def ranking():
#     # get user_ranking dictionary
#     user_ranking = r.zrange('user_ranking', 0, 1, desc=True)[:10]
#     user_ranking_ids = [int(id_) for id_ in user_ranking]
#     # get most viewed users
#     most_viewed = list(User.objects.filter(id__in=user_ranking_ids))
#     most_viewed.sort(key=lambda x: user_ranking_ids.index(x.id))
#     return most_viewed


def instructors(request, slug=None):
    instructors_ = Instructors.objects.all().order_by('order')
    if slug:
        instructor_ = Instructors.objects.get(slug=slug)
    else:
        instructor_ = Instructors.objects.all().order_by('order')[0]
    return render(request, 'partners/instructors.html', {
        'instructors': instructors_,
        'instructor': instructor_
    })


def instructor_tag(request, slug=None):
    instructors_ = Instructors.objects.all().order_by('order')
    tag = None
    if slug:
        try:
            tag = get_object_or_404(Tag, slug=slug)
            instructors_ = instructors_.filter(tags__in=[tag])
        except Exception as er:
            print(er)
    instructor_ = Instructors.objects.all().order_by('order')[0]
    return render(request, 'partners/instructors.html', {
        'instructors': instructors_,
        'instructor': instructor_,
        'tag': tag
    })


def partner_detail(request, slug):
    partner = Partners.objects.get(slug=slug)
    return render(request, 'partners/partner.html', {'partner': partner})




