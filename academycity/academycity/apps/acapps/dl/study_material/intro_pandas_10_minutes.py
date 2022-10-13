# https://pandas.pydata.org/docs/user_guide/10min.html
import pandas as pd
import numpy as np
import statistics as st

# s = pd.Series([1, 3, 5, np.nan, 6, 8])
# print(s)
#
# dates = pd.date_range("20130101", periods=6)
# print(dates)
# print(np.random.randn(6, 4))


def st_(l):

    print('l'*20)
    print(l)
    print('l'*20)

    print('-st'*10)
    print(st.stdev(l))
    print('-st'*10)

    m_ = sum(l) / len(l)

    print('-m'*10)
    print(m_)
    print('-m'*10)

    l_ = []
    for k in l:
        l_.append(k-m_)

    print('l_'*20)
    print(l_)
    print('l_'*20)

    print('---new m----')
    print(round(st.mean(l_)))
    print('---new m----')

    l__ = list(map(lambda x: x * x, l_))

    print('l__'*10)
    print(l__)
    print('l__'*10)

    va_ = sum(l__)/(len(l))

    eva_ = sum(l__)/(len(l)-1)

    est_=eva_**0.5

    return eva_, va_, est_

ll = [5, 5, 5, 5, 35, 5]
ev, v, s = st_(ll)

print('-st'*10)
print(ev, v, s)
print('-st'*10)


df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))
print(df)

df2 = pd.DataFrame(
    {
        "A": 1.0,
        "B": pd.Timestamp("20130102"),
        "C": pd.Series(1, index=list(range(4)), dtype="float32"),
        "D": np.array([3] * 4, dtype="int32"),
        "E": pd.Categorical(["test", "train", "test", "train"]),
        "F": "foo",
    }
)
print(df2)
print(df2.dtypes)
print(df.head())
print(df.tail(3))
print(df.index)
print(df.columns)
print(df.to_numpy())
print(df.describe())
print(df.T)
print(df.sort_index(axis=1, ascending=False))
print(df.sort_values(by="B"))
# Selection
df["A"]
df[0:3]
df["20130102":"20130104"]
# Selection by label
df.loc[dates[0]]
df.loc[:, ["A", "B"]]
df.loc["20130102":"20130104", ["A", "B"]]
df.loc["20130102", ["A", "B"]]
df.loc[dates[0], "A"]
df.at[dates[0], "A"]
# Selection by position
df.iloc[3]
df.iloc[3:5, 0:2]
df.iloc[[1, 2, 4], [0, 2]]
df.iloc[1:3, :]
df.iloc[:, 1:3]
df.iloc[1, 1]
df.iat[1, 1]
# Boolean indexing
df[df["A"] > 0]
df[df > 0]
df2 = df.copy()
df2["E"] = ["one", "one", "two", "three", "four", "three"]
df2
df2[df2["E"].isin(["two", "four"])]
# Setting
s1 = pd.Series([1, 2, 3, 4, 5, 6], index=pd.date_range("20130102", periods=6))
print(s1)
df["F"] = s1
df.at[dates[0], "A"] = 0
df.iat[0, 1] = 0
df.loc[:, "D"] = np.array([5] * len(df))
df
df2 = df.copy()
df2[df2 > 0] = -df2
df2
# Missing data


