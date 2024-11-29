import math
number = int(input("Enter a number: "))
sqrt_num = math.sqrt(number)
if number % 3 == 0 and number % 5 == 0 and sqrt_num.is_.integer():
    print("Fizz Buzz square")
elif number % 3 == 0:
    print("Fizz")
elif number % 5 == 0:
    print("Buzz")
elif sqrt_num.is_integer():
    print("This number is square! ")
else:print(f"{number} not a multiple of 5 or 3 or a square root! ")