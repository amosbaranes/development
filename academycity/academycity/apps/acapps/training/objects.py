from .models import Soldiers, DoubleShoot as DoubleShootModel
from django.http import JsonResponse
import requests


class TestManager(object):
    def __init__(self, dic=None):
        self.obj_dic = dic


class DoubleShoot(object):
    def __init__(self, dic=None):
        url_a = "https://qa.double-shoot.com/FlexiCore/rest/authenticationNew/login"
        a_dic = {"email": "amos@drbaranes.com", "password": "ynzVEPh9SrQf8Fgt"}
        self.authentication_key = requests.post(url_a, json=a_dic).json()["authenticationKey"]
        self.head = {'authenticationKey': '{}'.format(self.authentication_key)}
        self.url_ = "https://qa.double-shoot.com/FlexiCore/rest/plugins/Member/{}/{}"

    def get_soldier_data(self, dic=None):
        print(dic)
        ds_soldier_id = dic["ds_soldier_id"]
        function_name = dic["function_name"]
        # print("function name: ", function_name, "\nsoldier_id: ", soldier_id, "\n", "="*10)
        url_ = self.url_.format(function_name, ds_soldier_id)
        # print('\nurl_: ', url_, "\n", "="*10)
        return requests.get(url_, headers=self.head).json()

    # https://www.yellowduck.be/posts/outputting-django-queryset-json
    # print("need to get double shoot id")
    def update_or_get_soldier_data(self, dic=None):
        # print("-"*100, "\nupdate_or_get_soldier_data\n", dic, "\n", "-"*100)
        soldier_id = dic["soldier_id"]
        data = {
                'soldier_id': soldier_id,
                'double_shoot_id': "-1"
               }
        try:
            # print("90123-0 update_or_get_soldier_data 100\n", "solder_id: ", soldier_id, "\n", "-" * 100)
            soldier = Soldiers.objects.get(id=soldier_id)
            # print("90123-1 soldier obj: ", soldier)
            ds_row, is_created = DoubleShootModel.objects.get_or_create(soldier=soldier)
            data['double_shoot_id'] = ds_row.double_shoot_id
            # print(ds_row)
            # print("update_or_get_soldier_data 100-1", "\n", "-" * 100)
        except Exception as ex:
            print("90876-23: "+str(ex))
            data['double_shoot_id'] = "-100 error create record in ds model"
        # print('data 1')
        # print(data)
        # print('data 1')

        if not ds_row.is_pulled:
            try:
                # print(soldier_id)
                # print("Get data and update our system")
                function_name = dic["function_name"]
                ds_update_data = self.get_soldier_data({"ds_soldier_id": data['double_shoot_id'], "function_name": function_name})
                data["pulled_data"] = ds_update_data
                #
                # # # # update the DoubleShootModel with the pulled data.
                #
                ds_row.is_pulled = True
                ds_row.save()
            except Exception as ex:
                print("Error 9085-125 DoubleShoot update_or_get_soldier_data:\n"+ex)
                data['double_shoot_id'] = "-2"

        # update the data dictionary with data from our DoubleShootModel
        # print('data')
        # print(data)
        # print('data')

        return data

# double_shoot = DoubleShoot()
# # function = "getSolderData"
# dic = {"function_name": "getMember", "soldier_id": "RoxASKgvRGaR90ZuAnc3Gw"}
# r = double_shoot.get_soldier_data(dic)

