from .basic_algos import AlgoDLBase
# from tensorflow.keras.datasets import mnist
import yfinance as yf


class AlgoDL(AlgoDLBase):
    def __init__(self):
        super().__init__()

    def test(self, params):
        print("9010 input params: \n", params, "\n"+"-"*30)
        # (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

        # obj = yf.Ticker("^GSPC")
        obj = yf.Ticker(params["ticker"])
        # get historical market data
        hist = obj.history(
            #period="5d",
            interval="1m",
            start="2022-10-12", end="2022-10-13")
        # print('-1 ' *30)
        # print(hist)

        result = {"datetime": [], "close": []}
        for index, row in hist.iterrows():
            result["datetime"].append(str(index))
            result["close"].append(round(100*row["Close"])/100)

        output_dic = {'data': result}
        # print("9099 output dic: \n", output_dic, "\n"+"="*30)
        return output_dic

