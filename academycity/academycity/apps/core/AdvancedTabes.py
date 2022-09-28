from django.shortcuts import render
from django.http import JsonResponse
from django.apps import apps
from .models import DataAdvancedTabs, DataAdvancedTabsManager, AdjectivesValues, DataAdvancedApps


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

    def delete_record(self, params):
        try:
            # print(params)
            model = apps.get_model(app_label=params["app"], model_name=params["model"])
            obj = model.objects.get(id=params["id"])
            obj.delete()
            result = {'id': params["id"]}
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
                content_ = {"properties": {"tab_name": params["tab_name"], 'tab_order': 1,
                                           "tab_title": params["tab_name"],
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
            app_, c = DataAdvancedApps.objects.get_or_create(app_name=self.app)
            tabs = DataAdvancedTabs.objects.filter(manager=manager_).all()
            result = []
            for t in tabs:
                # print(t.id)
                # print('t.tab_content')
                content_ = t.tab_content
                content_["properties"]["tab_order"] = t.order
                content_["tab_order"] = t.order
                t.tab_content = content_
                t.save()
                result.append((t.id, t.tab_content))
            result = {"manager": manager_.manager_content, "tabs": result, "app_content": app_.app_content}
            # print(result)
        except Exception as ex:
            result = {"error": "-1"}
        return result

    def save_content(self, params):
        try:
            # print('='*50)
            # print('params')
            # print(params)
            # print('atm_content')
            # print(params["atm_content"])
            # print('='*20)
            # print('tab_content')
            # print(params["tab_content"])
            # print('='*20)
            # print('tab_name')
            # print(params["tab_name"])
            # print(params["app_content"])
            # print('='*50)
            try:
                atm = DataAdvancedTabsManager.objects.get(at_name=self.manager_name)
                atm.manager_content = params["atm_content"]
                atm.save()
                app = DataAdvancedApps.objects.get(app_name=self.app)
                app.app_content = params["app_content"]
                app.save()
                tab = DataAdvancedTabs.objects.get(manager=atm, id=params["tab_id"])
                tab.tab_content = params["tab_content"]
                tab.tab_name = params["tab_name"]
                tab.order = params["tab_order"]
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

    def get_adjective(self, params):
        # print('='*50)
        # print('params')
        # print(params)

        app_ = params['app']
        model_name_ = params['model_name']

        field_value_ = params['field_value']

        manager_name = params['manager_name']
        manager_fun = params['manager_fun']

        manager_fun_field = params['manager_fun_field']

        model = apps.get_model(app_label=app_, model_name=model_name_)

        s = "model." + manager_name + "." + manager_fun + "("+manager_fun_field+"=field_value_)"
        data = eval(s)
        # print(data)
        result = []
        for q in data:
            # print(q.order, q.id)
            result.append((q.id, q.value))
        # print('result')
        # print(result)
        # print('result')
        return result

    def get_list_from_model(self, params):
        # print('params')
        # print(params)

        app_ = params['app']
        model_name_ = params['model_name']
        field_name_ = params['field_name']

        model = apps.get_model(app_label=app_, model_name=model_name_)

        data_filter_field_ = params['data_filter_field']
        data_filter_field_value_ = params['data_filter_field_value']
        if data_filter_field_value_ or data_filter_field_value_ != "":
            try:
                data = eval('model.objects.filter('+data_filter_field_+'__icontains="'+data_filter_field_value_+'").all()')
            except Exception as ex:
                data = eval('model.objects.filter('+data_filter_field_+'__icontains='+data_filter_field_value_+').all()')
        else:
            data = model.objects.all()
        # print(data)
        result = []
        for q in data:
            s = 'result.append((q.id, q.'+field_name_+'))'
            eval(s)
        # print('result')
        # print(result)
        # print('result')
        return result

