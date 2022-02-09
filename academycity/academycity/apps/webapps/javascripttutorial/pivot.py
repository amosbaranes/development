import pandas as pd

df = pd.DataFrame({'foo': ['one', 'one', 'one', 'two', 'two', 'two'],
                   'bar': ['A', 'B', 'C', 'A', 'B', 'C'],
                   'baz': [1, 2, 3, 4, 5, 6],
                   'zoo': ['x', 'y', 'z', 'q', 'w', 't']})

print(df)
dfp = df.pivot(index='foo', columns='bar', values='baz')
print(dfp)


def adder(*num):
    sum = 0

    for n in num:
        sum = sum + n

    # print("Sum:", sum)


adder(3, 5, 4)
adder(4, 5, 6, 7)
adder(1, 2, 3, 5, 6)


def myFun(*argv):
    for arg in argv:
        print(arg)

myFun('Hello', 'Welcome', 'to', 'GeeksforGeeks')

def intro(**data):
    # print("\nData type of argument:",type(data))

    for key, value in data.items():
         print("{} is {}".format(key,value))


intro(Firstname="Sita", Lastname="Sharma", Age=22, Phone=1234567890)
intro(Firstname="John", Lastname="Wood", Email="johnwood@nomail.com", Country="Wakanda", Age=25, Phone=9876543210)

