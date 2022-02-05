def is_really_old(turtle):
    if turtle.age > 150:
        print(f'Woah, {turtle.name} is pretty old!')
    else:
        print('Nah')

class Animal:
    def __init__(self, name):
        self.name = name


class Turtle(Animal):
    def __init__(self, name, age):
        super().__init__(name)
        self.age = age

    def is_old(self):
        if self.age > 100:
            print (f'Woah, {self.name} is pretty old!')
        else:
            print('Nah')

greg = Turtle('gregory', 120)

is_really_old(greg)

greg.is_old()

boat = []
plane = []
if not boat:
    print('yup')

if len(boat) or len(plane) == 0:
    print('yup')


i = 25.9
print(int(i))
