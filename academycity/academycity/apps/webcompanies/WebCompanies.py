from .models import WebCompanies
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from ..core.utils import log_debug


class WebSiteCompany(object):
    def __init__(self, request, domain=None, web_company_id=None, is_test=False):
        # if web_company_id:
        #     log_debug("Create WebSiteCompany for: "+str(web_company_id))
        # if domain:
        #     log_debug("Create WebSiteCompany for domain_0: "+str(domain))
        # print('-1 '*20)
        # print('WebSiteCompany--'*3)
        # print('-1'*20)
        self.web_company_id = -1
        if domain:
            # print('-domain '*5)
            # print(domain)
            # log_debug("Create WebSiteCompany for domain_0: "+str(domain))
            # print('-domain '*5)
            try:
                # log_debug('WebSiteCompany domain1: ' + domain)
                web_company_ = WebCompanies.objects.get(domain=domain)
                log_debug('WebSiteCompany web_company_ found_2: ')
                self.web_company_id = web_company_.id
                log_debug('WebSiteCompany web_company_ found_30: ' + str(web_company_id))
                log_debug('WebSiteCompany web_company_ found_31: ' + str(self.web_company_id))
                app_label_ = web_company_.target_ct.app_label
                log_debug('WebSiteCompany web_company_ found app_label_4 : ' + app_label_)
                request.session[settings.WEB_SITE_COMPANY_ID] = {'domain': domain,
                                                                 'web_company_id': self.web_company_id,
                                                                 'app_label': app_label_}
            except Exception as ex:
                # print('-domain ex'*5)
                # print(ex)
                # print('-domain ex'*5)
                request.session[settings.WEB_SITE_COMPANY_ID] = {'domain': 'null'}

        # print("1234-1", settings.WEB_SITE_COMPANY_ID)
        try:
            self.web_site_company = request.session[settings.WEB_SITE_COMPANY_ID]
        except Exception as ex:
            print("="*50)
            print(str(ex))
            print("="*50)

        if (not is_test) and self.is_registered_domain():
            self.web_company_id = self.web_site_company['web_company_id']
        elif web_company_id:
            self.web_company_id = web_company_id

        # print('WebSiteCompany-web_company_id')

        log_debug("WebSiteCompany created for web_company_id: " + str(self.web_company_id))
        # print(web_company_id)
        # print('-' * 20)

    def is_registered_domain(self):

        # print('self.web_site_company')
        # print(self.web_site_company)
        # print('self.web_site_company')
        # print(self.web_site_company['domain'] != 'null')

        return self.web_site_company['domain'] != 'null'

    def get_redirect_link(self):
        return HttpResponseRedirect(reverse(self.web_site_company['app_label'] + ':home'))

    def add(self, request, key, value):
        # print('add')
        # print('add')
        # print('add')
        if self.is_registered_domain():
            self.web_site_company[key] = value
        else:
            # print('add else')
            if not request.session[settings.WEB_SITE_COMPANY_ID]:
                request.session[settings.WEB_SITE_COMPANY_ID] = {key: value}
            else:
                # print('add else else')
                # print(request.session[settings.WEB_SITE_COMPANY_ID])
                request.session[settings.WEB_SITE_COMPANY_ID][key] = value
                # print('request.session[settings.WEB_SITE_COMPANY_ID]')
                # print(request.session[settings.WEB_SITE_COMPANY_ID])
        request.modified = True

    def get(self, key):
        return self.web_site_company[key]

    def site_company(self, model='', web_company_id=None):
        try:
            if web_company_id:
                web_company = WebCompanies.objects.get(id=web_company_id)
            else:
                web_company = WebCompanies.objects.get(id=self.web_company_id)
            # print('site_company - web_company')
            # print(web_company)

            if model != '':
                s = "objs = web_company.target."+model+".filter(is_active=True).all()"
                dic_ = {'web_company': web_company}
                exec(s, dic_)
                objs = dic_['objs']
            else:
                objs = web_company.target

        except Exception as ex:
            log_debug("Exception WebSiteCompany: "+str(ex))
            # print(ex)
        return objs
