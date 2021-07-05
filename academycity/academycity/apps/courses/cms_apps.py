# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


@apphook_pool.register  # register the application
class CoursesApp(CMSApp):

    app_name = 'courses'

    name = _('Courses')

    def get_urls(self, page=None, language=None, **kwargs):
        return ["academycity.apps.courses.urls"]

