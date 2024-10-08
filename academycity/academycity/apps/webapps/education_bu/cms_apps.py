# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


@apphook_pool.register  # register the application
class EducationApp(CMSApp):

    app_name = 'education'

    name = _('Education')

    def get_urls(self, page=None, language=None, **kwargs):
        return ["academycity.apps.education.urls"]

