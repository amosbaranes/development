from .models import Friends as friends


class Friends(object):
    def __init__(self):
        pass

    def update_friends_list(self, dic):
        # print("9055 \n")

        # print("-"*50)
        # print("-"*50)
        # print(dic["name"])
        # print("-"*10)
        # print(dic["data"])
        # print("-"*10)
        try:
            if len(dic["data"]) == 0:
                friends.objects.get(name=dic["name"]).delete()
            else:
                row, is_created = friends.objects.get_or_create(name=dic["name"])
                # print(is_created)
                row.friends = dic["data"]
                row.save()
        except Exception as ex:
            print(str(ex))
        # save to table
        # results = {"status": "ko"}
        # print("-"*50)
        # print("-"*50)
        # save to database
        results = {"status": "ok"}
        return results

    def get_friends_list(self, dic):
        # print("9055 \n")
        # print("-"*50)
        # print("-"*50)
        # print(dic["name"])
        try:
            row = friends.objects.get(name=dic["name"])
            data = row.friends
            # print(data)
            # print("exist")
        except Exception as ex:
            data = []
            # print("not exist")
        # get data from table in
        # results = {"status": "ko"} result dictionary
        # print("-"*50)
        # print("-"*50)
        # save to database
        results = {"status": "ok", "data": data}
        return results

    def test(self, dic):
        print(dic)
        # if i wnt to do something this is the place
        data = {"a": "b"}
        return {"status": "ok", "data": data}
