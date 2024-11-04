# Coffee prices
coffee_prices = {
    "Espresso": 2.50,
    "Americano": 3.00,
    "Latte": 2.50,
    "Cappuccino": 3.00,
    "Macchiato": 2.50,
    "Mocha": 3.50,
    "Flat White": 2.50,
}

# Welcome message
print("The Coffee Shop\nWelcome")
print("We serve the following coffees:")
for coffee in coffee_prices:
    print(f" > {coffee}")

# Ask for coffee choice
coffee = input("What coffee would you like? ")

if coffee not in coffee_prices:
    print("Sorry, we don't serve that coffee.")
else:
    size = int(input("What size would you like (1, 2, 3)? "))
    
    if size not in (1, 2, 3):
        print("You cannot pick a number bigger than 3 or less than 1.")
    else:
        print(f"You have chosen size {size}.")
        
        total = coffee_prices[coffee] + (0.50 if size == 2 else 1.00 if size == 3 else 0)
        print(f"The total price for your {size} size {coffee} is ${total:.2f}.")
