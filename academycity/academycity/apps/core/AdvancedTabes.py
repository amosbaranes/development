from django.shortcuts import render
from django.http import JsonResponse
from .models import DataAdvancedTabs, DataAdvancedTabsManager


class AdvancedTabs(object):
    def __init__(self, manager_name, app):
        self.manager_name = manager_name
        self.app = app

    def delete_tab(self, params):
        try:
            # print('-2'*10)
            # print(params)
            # print('-2'*10)
            tab_name_ = params["tab_name"]
            tab_to_delete = DataAdvancedTabs.objects.get(manager__at_name=self.manager_name, tab_name=tab_name_)
            tab_id_ = tab_to_delete.id
            tab_to_delete.delete()
            result = {'tab_id': tab_id_}
        except Exception as ex:
            result = {'tab_id': "-1"}
        return result

    def add_tab(self, params):
        try:
            # print('-1'*10)
            # print(params)
            # print('-1'*10)
            tab_name_ = params["tab_name"]
            manager_, n_ = DataAdvancedTabsManager.objects.get_or_create(at_name=self.manager_name)
            if n_:
                manager_.manager_content = {"last_obj_number": 0}
                manager_.save()
            t, n_ = DataAdvancedTabs.objects.get_or_create(manager=manager_, tab_name=tab_name_)
            try:
                content_ = {"properties": {"tab_name": params["tab_name"], "tab_title": params["tab_name"],
                            "tab_type": "empty"}}
                # print(content_)
                t.tab_content = content_
                t.save()
            except Exception as ex:
                print(ex)
            result = {t.id: t.tab_content}
        except Exception as ex:
            result = {'error': "-1"}
        return result

    def get_tabs_from_table(self, params):
        try:
            manager_ = DataAdvancedTabsManager.objects.get(at_name=self.manager_name)
            tabs = DataAdvancedTabs.objects.filter(manager=manager_).all()
            result = {}
            for t in tabs:
                # print(t.id)
                # print('t.tab_content')
                result[t.id] = t.tab_content
            # print("ok")
            result = {"manager": manager_.manager_content, "tabs": result}
            # print(result)
        except Exception as ex:
            result = {"error": "-1"}
        return result

    def save_content(self, params):
        try:
            # print('='*50)
            # print('params')
            # print(params)
            # print('='*20)
            # print('atm_content')
            # print(params["atm_content"])
            # print('='*20)
            # print('tab_content')
            # print(params["tab_content"])
            # print('='*20)
            # print('tab_name')
            # print(params["tab_name"])
            # print('='*50)
            try:
                atm = DataAdvancedTabsManager.objects.get(at_name=self.manager_name)
                atm.manager_content = params["atm_content"]
                atm.save()
                tab = DataAdvancedTabs.objects.get(manager=atm, id=params["tab_id"])
                tab.tab_content = params["tab_content"]
                tab.tab_name = params["tab_name"]
                tab.save()
                # print("saved")
            except Exception as ex:
                print(ex)
            # print(tab)
            # print('='*50)
            result = {"saved": "ok"}

        except Exception as ex:
            result = {"error": "-1"}
        return result
