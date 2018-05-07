class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def work(self): print("%s goes to work" % self.name)


class Employee(Person):
    def __init__(self, name, age, job):
        super(Employee, self).__init__(name, age)
        self.job = job

    def get_paid(self): print("%s gets a paycheck" % self.name)


class Programmer(Employee):
    def __init__(self, name, age, lang):
        super(Programmer, self).__init__(name, age, "Programmer")
        self.coding_language = lang

    def code(self): print("%s goes to code a game with %s" % (self.name, self.coding_language))


Bob = Person("Bob", 30)
Joe = Employee("Joe", 36, "Store Clerk")
Jim = Programmer("Jim", 434343433333433434343, "C++")

Bob.work()
Joe.get_paid()
Jim.code()
