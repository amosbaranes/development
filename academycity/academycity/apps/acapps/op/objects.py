import math

class Option(object):
    def __init__(self):
        pass

    def call(self, S, K, T, r, sigma, n):
        dt = T / n
        u = math.exp(sigma * math.sqrt(dt))
        d = 1 / u
        p = (math.exp(r * dt) - d) / (u - d)
        option_price_c = [max(0, S * (u ** (n - i)) * (d ** i) - K) for i in range(n + 1)]

        for j in range(n - 1, -1, -1):
            for i in range(j + 1):
                option_price_c[i] = max(S * (u ** (j - i)) * (d ** i) - K,
                                        math.exp(-r * dt) * (
                                                    p * option_price_c[i] + (1 - p) * option_price_c[i + 1]))

        return round(100 * option_price_c[0]) / 100

    def put(self, S, K, T, r, sigma, n):
        dt = T / n
        u = math.exp(sigma * math.sqrt(dt))
        d = 1 / u
        p = (math.exp(r * dt) - d) / (u - d)

        option_price_p = [max(0, K - S * (u ** (n - i)) * (d ** i)) for i in range(n + 1)]

        for j in range(n - 1, -1, -1):
            for i in range(j + 1):

                option_price_p[i] = max(K - S * (u ** (j - i)) * (d ** i),
                                        math.exp(-r * dt) * (
                                                    p * option_price_p[i] + (1 - p) * option_price_p[i + 1]))

        return round(100 * option_price_p[0]) / 100


    def test1(self, dic):
        print('90-90-90-11 data_transfer_to_process_fact 90055-300 dic\n', '-'*100, '\n', dic, '\n', '-'*100)
        app_ = dic["app"]
        # S = float(dic["S"])
        K = float(dic["K"])
        sigma = float(dic["sigma"])
        T = int(dic["T"])
        r = float(dic["r"])
        n = int(dic["n"])
        t = int(dic["t"])
        T = T-t/n

        x=[]
        lp=[]
        lc=[]
        for i in range(1, 200, 1):
            c = self.call(i, K, T, r, sigma, n)
            p = self.put(i, K, T, r, sigma, n)
            x.append(i)
            lc.append(c)
            lp.append(p)

        # print(lc, lp)

        result = {"status": "ok", "data": {"x":x, "lc":lc, "lp":lp}}
        return result
