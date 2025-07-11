# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from django.urls import path, include, re_path

# from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {'cmspages': CMSSitemap}}),
]

urlpatterns += i18n_patterns(
    url(r'^admin/', admin.site.urls),  # NOQA
    url('^rosetta/', include('rosetta.urls')),
    url(r'core/', include('academycity.apps.core.urls')),

    url(r'actions/', include('academycity.apps.actions.urls')),
    url(r'images/', include('academycity.apps.images.urls')),
    url(r'ueconomics/', include('academycity.apps.ueconomics.urls')),
    url(r'elaerning/', include('academycity.apps.elearning.urls')),

    # url(r'partners/', include('academycity.apps.partners.urls')),
    # url(r'courses/', include('academycity.apps.courses.urls')),

    # url(r'users/', include('academycity.apps.users.urls')),

    # re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),  # < here
    url(r'shop/', include('academycity.apps.shop.urls')),
    url('cart/', include('academycity.apps.cart.urls')),
    url('orders/', include('academycity.apps.orders.urls', namespace='orders')),
    url('payment/', include('academycity.apps.payment.urls', namespace='payment')),

    url(r'blog/', include('academycity.apps.blog.urls')),
    url(r'globsim/', include('academycity.apps.globsim.urls')),
    url(r'corporatevaluation/', include('academycity.apps.corporatevaluation.urls')),
    url(r'polls/', include('academycity.apps.polls.urls')),
    url(r'research/', include('academycity.apps.research.urls')),
    path(r'search/', include('academycity.apps.search.urls')),

    url(r'^chat/', include('academycity.apps.chat.urls')),
    url(r'^videocall/', include('academycity.apps.videocall.urls')),
    # url(r'^drbaranes/', include('academycity.apps.drbaranes.urls')),
    url(r'^u/', include('academycity.apps.ugandatowns.urls')),

    url(r'^openvidu/', include('academycity.apps.openvidu.urls')),
    #
    url(r'^webcompanies/', include('academycity.apps.webcompanies.urls')),
    #
    #
    url(r'acmath/', include('academycity.apps.acapps.acmath.urls')),
    url(r'avi/', include('academycity.apps.acapps.avi.urls')),
    url(r'avia/', include('academycity.apps.acapps.avia.urls')),
    url(r'avib/', include('academycity.apps.acapps.avib.urls')),
    url(r'avic/', include('academycity.apps.acapps.avic.urls')),

    url(r'arthur/', include('academycity.apps.acapps.arthur.urls')),
    url(r'covid/', include('academycity.apps.acapps.covid.urls')),
    url(r'nces/', include('academycity.apps.acapps.nces.urls')),

    url(r'case1/', include('academycity.apps.acapps.case1.urls')),

    url(r'el/', include('academycity.apps.acapps.el.urls')),
    url(r'ao/', include('academycity.apps.acapps.ao.urls')),
    url(r'potential/', include('academycity.apps.acapps.potential.urls')),
    url(r'fuzzyforcast/', include('academycity.apps.acapps.fuzzyforcast.urls')),
    url(r'mm/', include('academycity.apps.acapps.mm.urls')),
    url(r'ms/', include('academycity.apps.acapps.ms.urls')),
    url(r'nu/', include('academycity.apps.acapps.nu.urls')),
    url(r'op/', include('academycity.apps.acapps.op.urls')),
    url(r'training/', include('academycity.apps.acapps.training.urls')),
    url(r'dl/', include('academycity.apps.acapps.dl.urls')),
    url(r'ml/', include('academycity.apps.acapps.ml.urls')),
    url(r'businesssim/', include('academycity.apps.acapps.businesssim.urls')),
    url(r'accounting/', include('academycity.apps.acapps.accounting.urls')),
    url(r'l/', include('academycity.apps.acapps.liongold.urls')),
    #

    url(r'c/', include('academycity.apps.webapps.checkcashingchicago.urls')),
    url(r'e/', include('academycity.apps.webapps.education.urls')),
    url(r'p/', include('academycity.apps.webapps.portfolio.urls')),
    url(r'^f/', include('academycity.apps.webapps.fabhouseafrica.urls')),
    url(r'r/', include('academycity.apps.webapps.radiusfood.urls')),
    url(r'b/', include('academycity.apps.webapps.bizland.urls')),
    url(r'a/', include('academycity.apps.webapps.apewives.urls')),
    url(r'j/', include('academycity.apps.webapps.javascripttutorial.urls')),
    url(r's/', include('academycity.apps.webapps.simba.urls')),
    #
    url(r'^swotclock/', include('academycity.apps.webapps.swotclock.urls')),
    #
    url(r'^allauth/', include('allauth.urls')),
    url(r'^', include('cms.urls')),
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ] + staticfiles_urlpatterns() + urlpatterns

    #  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

