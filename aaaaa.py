def add(index, value):
    x[index - 1] += value

def subtraction(index, value):
    x[index - 1] -= value

x = [10, 0, 0, 0, 0]
while True:
    print("x = [ ", end="")
    for i in range(len(x)):
        print("{} ".format(x[i]), end="")
    print("]")

    f = int(input("from (終了は99と入力):"))
    if f==99:
        print("処理を終了します. ")
        break
    else:
        t = int(input("to:"))
        v = int(input("value:"))
        add(t, v)
        subtraction(f, v)