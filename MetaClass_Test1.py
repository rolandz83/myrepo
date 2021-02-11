from datetime import datetime
import time

'''
Why meta class runs only once ?
Why both datetime stamps are the same ?
How can I pass class object attr to a metaclass ?
'''

def get_instantiation_time(self):
    return self.instantiation_time

class My_Meta(type):
    listofinst = []
    def __new__(mcs, name, bases, attrs):
        object = super().__new__(mcs, name, bases, attrs)
        print("datetime object created...")
        object.instantiation_time = datetime.now()
        object.get_instantiation_time = get_instantiation_time
        print("FROM META CLASS", attrs['temp'])
        return object

class Student(metaclass=My_Meta):
    temp = 5
    def __init__(self, name, age):
        self.name = name
        self.age = age

print("Time now is: ", datetime.now())
time.sleep(2)
student_A = Student('john', 15)

print("Time now is: ", datetime.now())
time.sleep(3)
print("Student named {} signed up to school".format(student_A.name))

print("Time now is: ", datetime.now())
student_B = Student('marry', 14)
print("Student named {} signed up to school".format(student_B.name))

print("Time now is: ", datetime.now())
print("Student A signed up at: ", student_A.get_instantiation_time())
print("Student B signed up at: ", student_B.get_instantiation_time())

print("Metal class list: ", My_Meta.listofinst)
