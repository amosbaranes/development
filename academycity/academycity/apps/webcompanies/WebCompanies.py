from .models import WebCompanies
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from ..core.utils import log_debug


class WebSiteCompany(object):
    def __init__(self, request, domain=None, web_company_id=None):
        # print('-1'*20)
        self.web_company_id = -1
        if domain:
            # print('-2'*20)
            try:
                # log_debug('WebSiteCompany domain: ' + domain)
                web_company_ = WebCompanies.objects.get(domain=domain)
                # log_debug('WebSiteCompany web_company_ found: ')
                self.web_company_id = web_company_.id
                # log_debug('WebSiteCompany web_company_ found: ' + str(web_company_id))
                app_label_ = web_company_.target_ct.app_label
                # log_debug('WebSiteCompany web_company_ found app_label_ : ' + app_label_)
                request.session[settings.WEB_SITE_COMPANY_ID] = {'domain': domain, 'web_company_id': self.web_company_id,
                                                                 'app_label': app_label_}
            except Exception as ex:
                # print('-20'*20)
                request.session[settings.WEB_SITE_COMPANY_ID] = None

        # print(11)
        self.web_site_company = request.session[settings.WEB_SITE_COMPANY_ID]
        # print(settings.WEB_SITE_COMPANY_ID)

        # print(self.is_registered_domain())
        # print(web_company_id)

        if not self.is_registered_domain() and web_company_id:
            # print('-3' * 20)
            # print(web_company_id)
            self.web_company_id = web_company_id

        # print('-4' * 20)
        # print('-4' * 20)

    def is_registered_domain(self):
        return self.web_site_company is not None

    def get_redirect_link(self):
        return HttpResponseRedirect(reverse(self.web_site_company['app_label'] + ':home'))

    def add(self, request, key, value):
        if self.is_registered_domain():
            self.web_site_company[key] = value
        else:
            if not request.session[settings.WEB_SITE_COMPANY_ID]:
                request.session[settings.WEB_SITE_COMPANY_ID] = {key: value}
            else:
                request.session[settings.WEB_SITE_COMPANY_ID]['key'] = value
        request.modified = True

    def get(self, key):
        return self.web_site_company[key]

    def site_company(self, model=''):
        try:
            if self.is_registered_domain():
                self.web_company_id = self.web_site_company['web_company_id']
            web_company = WebCompanies.objects.get(id=self.web_company_id)
        except Exception as ex:
            print(ex)

        if model != '':
            s = "objs = web_company.target."+model+".filter(is_active=True).all()"
            dic_ = {'web_company': web_company}
            exec(s, dic_)
            objs = dic_['objs']
        else:
            objs = web_company.target
        return objs
