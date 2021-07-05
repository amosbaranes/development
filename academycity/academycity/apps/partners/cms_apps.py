# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


@apphook_pool.register  # register the application
class PartnersApp(CMSApp):

    app_name = 'partners'

    name = _('Partners')

    def get_urls(self, page=None, language=None, **kwargs):
        return ["academycity.apps.partners.urls"]


@apphook_pool.register  # register the application
class InstructorsApp(CMSApp):

    app_name = 'partners'

    name = _('Instructors')

    def get_urls(self, page=None, language=None, **kwargs):
        return ["academycity.apps.partners.urls_instructor"]

