"""
# Devin

a = 4
b = 3

print(3 + 5)
print(5 -3)
print(3 * 5)
print(6 / 2)
print(3 ** 2)

print("Try to figure out how this works")
print(13 % 12)

car_name = "Wiebe Mobile"
car_type = "BMW"
car_cylinders = 8
car_mpg = 5000.9

print("I have a car called %s. It's pretty nice." % car_name)
print("I have a car called %s. It's a %s." % (car_name, car_type))
                                              # Watch the order!

print("What is your name?")
name = input(">_ ")
print("Hello %s" % name)

age = input("How old are you?")

print("%s?! That's really old. You belong in a retirement hom." % age)

def print_hw():
    print("Hello World.")
    print("Enjoy the day.")



def say_hi(name):
    print("Hello %s" % name)
    print("Coding is great!")



def print_age(name, age):
    print("%s is %d years old" % (name, age))
    age = age + 1
    print("Next year, %s will be %d years old" % (name, age)

def algebra_hw(x):
    return x ** 3 + 4 + x + +2 + 7 * x - 4

def grade_calc(percentage):
    if percentage >= 90:
        return "A"
    elif percentage >= 80:
        return "B"
    elif percentage >= 70:
        return "C"
    elif percentage >= 60:
        return "D"
    elif percentage >= 50:
        return "F"

print(grade_calc(90))

def happy_bday(name):
    print("Happy Birthday to you! \nHappy Birthday to you! \nHappy Birthday dear %s! \nHappy Birthday to you!" % name)


happy_bday("Devin")

# Loops

for i in range(0, 11):
    print(i)

a = 1
while a < 10:
    print(a)
    a += 1


# Random Numbers
import random #This should be on line 1
print(random.randint(0, 1000))

c = '1'
print(c == 1) # False: comparing different strings; string ≠ integer
print(int(c) == 1)
print(c == str(1))

# Comparisons
print(1 == 1) # Use a double equal sign (==)
print(1 != 2) # 1 is not equal to 2

# Lists
count = [1, 2, 3, 4, 5]
cheeseburger_ingredients = ['cheese', 'beef', 'sauce', 'sesame seed bun', 'avocado', 'onion']
# print(cheeseburger_ingredients[0])
# print(cheeseburger_ingredients[3])
# print(len(cheeseburger_ingredients))
# print(len(count))

# Going through lists
for num in cheeseburger_ingredients:
    print(num)

for num in count:
    print(num * 2)

length = len(cheeseburger_ingredients)
range(5) # list w/ numbers 0 - 4
range(len(cheeseburger_ingredients)) # generates a list of all indices

for num in range(len(cheeseburger_ingredients)):
    item = cheeseburger_ingredients[num]
    print("The item at index %d is %s." % (num, item))

# Recasting into a list
strOne = "Hello World!"
listOne = list(strOne)
print(listOne)
listOne[11] = '.'
print(listOne)
print(listOne[-1])


# Adding things to a list
cheeseburger_ingredients.append("Fries")
print(cheeseburger_ingredients)
cheeseburger_ingredients.append("burger")
print(cheeseburger_ingredients)
cheeseburger_ingredients.pop(1)
print(cheeseburger_ingredients)
cheeseburger_ingredients.remove("cheese")
print(cheeseburger_ingredients)

# Getting the alphabet
import string
print(string.ascii_letters)
print(string.ascii_lowercase)
print(string.punctuation)

# Making things Lowercase
str2 = "ThIs iS a vEry oDd seNTencE"
print(str2.lower())

# Inheritance


class Vehicle(object):
    def __init__(self, source, material, seat, speed, passengers):
        self.power_source = source
        self.material = material
        self.seat_location = seat
        self.max_speed = speed
        self.passengers = passengers

    def move(self): print("You move forward")

    def change_direction(self): print("You change directions")


class Car(Vehicle):
    def __init__(self, material, seat, speed, passengers, windows):
        super(Car, self).__init__('engine', material, seat, speed, passengers)
        self.windows = windows

    def roll_down_windows(self): print("you roll the windows down")

    def turn_on(self): print("You turn the key and the engine starts")


test_car = Car("Aluminum", 'Driver side', 140, 2, True)
# test_car.change_direction()


class KeylessCar(Car):
    def __init__(self, material, seat, speed, passengers, windows):
        super(KeylessCar, self).__init__(material, seat, speed, passengers, windows)

    def turn_on(self): print("You push the button and the car turns on.")


# test_car.turn_on()
cool_car = KeylessCar("Aluminum", 'Driver side', 140, 2, True)
# cool_car.turn_on()


class Tesla(Car):
    def __init__(self, material, seat, speed, passengers, windows):
        super(Tesla, self).__init__(material, seat, speed, passengers, windows)

    def fly(self): print("You launch the car into low earth orbit")

    def turn_on(self): Car.turn_on(self)
"""
