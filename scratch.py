# from abc import ABC, abstractmethod

# class Animal(ABC):

#   @abstractmethod
#   def speak(self):
#     pass

# class Dog(Animal):
#   def speak(self):
#     return "Woof!"
  
# class Cat(Animal):
#   def speak(self):
#     return "Meow!"
  
# cat = Cat().speak() # you must create an instance and call the method on the instance in order for it to print from the function

# print(cat)

# class BankAccount:
#   def __init__(self, balance):
#     self.__balance = balance

#   def deposit(self,amount):
#     if amount > 0:
#       self.__balance += amount

#   def get_balance(self):
#     return self.__balance

# class SmartDevice:
#   def __init__(self, device_name):
#     self.device_name = device_name
#     self.status = False

#   def toggle(self):
#     self.status = not self.status
#     return self.status

# class SmartLight(SmartDevice):
#   def __init__(self,device_name):
#     super().__init__(device_name)
#     self.brightness = 0

#   def dimmer(self,brightness_level):
#     if 0 <= brightness_level <= 100:
#       self.brightness = brightness_level
#     else:
#       raise ValueError

#   def name(self):
#     return self.device_name


# smart = SmartLight("SmartLights")

# print(smart.toggle())
# print(smart.toggle())

# print(type(1+0.0))
# print(type(0.1))
# print(type(1))
# print(type(3/5))
# print(0.1+0.2)

# print(0.3 == (1+2)/10)

# a = [1,2]
# b = [3,4]

# c = a+b
# print(c)

# s = 'Hi my name is Sami'

# print(s.lower())

x = ['1','2','3','4']

new = "".join(x)

print(new)