#!/usr/bin/env python3


class Employee:
    def __init__(self, first, last):
        self.first = first
        self.last = last
        self.email = first + "." + last + "@email.com"

    @property
    def fullname(self):
        return f"{self.first} {self.last}"

    @property
    def property_email(self):
        return f"{self.first}.{self.last}@email.com"

    @fullname.setter
    def fullname(self, name):
        first, last = name.split(" ")
        self.first = first
        self.last = last

    @fullname.deleter
    def fullname(self):
        print("Delete name!")
        self.first = None
        self.last = None


def main():
    me = Employee("Jai", "Lak")
    me.first = "Shiv"
    print(me.first, me.last, me.fullname)
    # Notice email did not get updated
    # Should use getter/setter methods or property decorator method
    print(me.email)
    # Using the property decorator method
    print(me.property_email)

    # Set fullname property method using fullname.setter method
    me.fullname = "Jai Lak"
    print(me.first, me.last, me.fullname, me.property_email)

    # Delete name using fullname.deleter method
    del me.fullname
    print(me.first, me.last, me.fullname, me.property_email, me.email)


if __name__ == "__main__":
    main()
