from django.shortcuts import render
from django.http import JsonResponse
from .models import DataAdvancedTabs


class AdvancedTabs(object):
    def __init__(self, manager_name):
        self.manager_name = manager_name

    def delete_tab(self, params):
        try:
            print('-'*10)
            print(params)
            print('-'*10)
            tab_name_ = params["tab_name"]
            tab_to_delete = DataAdvancedTabs.objects.get(at_name=self.manager_name, tab_name=tab_name_)
            tab_id_ = tab_to_delete.id
            tab_to_delete.delete()
            result = {'tab_id': tab_id_}
        except Exception as ex:
            result = {'tab_id': "-1"}
        return result

    def add_tab(self, params):
        try:
            tab_name_ = params["tab_name"]
            new_tab, is_new_row = DataAdvancedTabs.objects.get_or_create(at_name=self.manager_name, tab_name=tab_name_)
            result = {'tab_id': new_tab.id}
        except Exception as ex:
            result = {'tab_id': "-1"}
        return result

    def get_tabs_from_table(self, params):
        try:
            tabs = DataAdvancedTabs.objects.filter(at_name=self.manager_name).all()
            result = {}
            for t in tabs:
                result[t.id] = {"tab_name": t.tab_name, "tab_text": t.tab_text, "tab_functions": t.tab_functions}
        except Exception as ex:
            result = {"error": "-1"}
        return result
