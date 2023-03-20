from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Animal(ABC):
    name: str
    
    def print_name(self):
        print(self.name)
        
    @abstractmethod
    def make_sound(self):
        pass
    
class Dog(Animal):
    def make_sound(self):
        print('WOOOF')

class Cat(Animal):
    def make_sound(self):
        print('MEOW')

@dataclass
class Animals:
    arr: list[Animal]

dog = Dog('Дружок')
cat = Cat('Снежок')
animals = Animals([dog, cat])
animals.arr[0].print_name()
animals.arr[0].make_sound()
animals.arr[1].print_name()
animals.arr[1].make_sound()
