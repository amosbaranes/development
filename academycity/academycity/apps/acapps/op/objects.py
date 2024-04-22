

class Option(object):
    def __init__(self):
        pass

    def call_price(self, dic):
        pass

    def test1(self, dic):
        print('90-90-90-11 data_transfer_to_process_fact 90055-300 dic\n', '-'*100, '\n', dic, '\n', '-'*100)
        app_ = dic["app"]
        s_ = float(dic["S"])

        print(app_, s_)


        result = {"status": "ok", "data": {"b":"c"}}
        return result
