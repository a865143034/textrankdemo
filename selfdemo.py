#coding=utf-8
class Person:
    def __init__(self,name):
        self.name=name
    def sayhello(self):
        print('Hello, my name is:',self.name)
p=Person('Bill')
p.sayhello()