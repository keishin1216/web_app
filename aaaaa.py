import math

while True:
    money = int(input("元金を入力してください: "))
    rate = float(input("利率を入力してください (例: 5 は 5%): ")) / 100
    long = int(input("期間を入力してください: "))
    if long > 0:
        break

def calculate_simple_interest(principal, interest_rate, years):
    return principal * (1 + interest_rate * years)

def calculate_compound_interest(principal, interest_rate, years):
    return principal * (1 + interest_rate)**years

def main():
    simple_balance = calculate_simple_interest(money, rate, long)
    compound_balance = calculate_compound_interest(money, rate, long)

    print(f"{long}年後の単利の残高: {math.floor(simple_balance)}")
    print(f"{long}年後の複利の残高: {math.floor(compound_balance)}")

    if compound_balance > simple_balance:
        print(f"{long}年目で複利が単利を超えました。")
    else:
        print(f"{long}年目でも複利は単利を超えませんでした。")

if __name__ == "__main__":
    main()
