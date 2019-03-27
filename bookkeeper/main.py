import os
import sys

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Student:
    def __init__(self, name, phone_number, marks):
        self.name = name
        self.phone_number = phone_number
        self.marks = marks

    def update_name(self, new_name):
        self.name = new_name

    def update_phone_number(self, new_phone_number):
        self.phone_number = new_phone_number

    def update_marks(self, marks):
        self.marks = marks


class Book:
    def __init__(self, path, student_list=[]):
        self.student_list = student_list
        self.path = path

    def write(self):
        with open(self.path, 'w+') as f:
            for s in self.student_list:
                line = "{},{},{},{},{}\n".format(
                    s.name, s.phone_number, s.marks[0], s.marks[1], s.marks[2])
                f.write(line)

    def read(self):
        self.student_list = []

        with open(self.path, 'r+') as f:
            content = f.readlines()

        for line in content:
            params = line.strip().split(',')
            s = Student(params[0], params[1], [float(
                params[2]), float(params[3]), float(params[4])])
            self.student_list.append(s)


def get_marks():
    marks = []
    for i in range(3):
        valid = False
        while not valid:
            m = input("Enter marks {}: ".format(i))
            try:
                marks.append(float(m))
            except Exception:
                print("Invalid input.")
            else:
                valid = True
    return marks


class MenuDriven:
    def __init__(self):
        self.book = Book(os.path.join(__location__, 'SAVE.txt'), [])
        self.book.read()

    def main_menu(self):
        print("1. Add\n2. Edit\n3. Delete\nq. Quit\n")
        opt = input()
        if opt == '1':
            self.add_screen()
        if opt == '2':
            self.edit_screen()
        if opt == '3':
            self.delete_screen()
        if opt == 'q':
            sys.exit()

    def enter_details(self):
        name = input("Enter Name: ")
        phone_number = input("Enter Phone Number: ")
        marks = get_marks()
        student = Student(name, phone_number, marks)

        return student

    def add_screen(self):
        student = self.enter_details()
        self.book.student_list.append(student)
        self.book.write()

        self.main_menu()

    def edit_screen(self):
        match = None
        while match is None:
            name = input("Find by Name: (q to go back) ")
            if name.strip() == 'q':
                self.main_menu()
                return
            for s in self.book.student_list:
                if s.name.lower() == name.lower():
                    match = s
                    break
            if match is None:
                print("Could not find student named- {}".format(name))

        self.book.student_list.remove(match)
        student = self.enter_details()
        self.book.student_list.append(student)
        self.book.write()

        self.main_menu()

    def delete_screen(self):
        match = None
        while match is None:
            name = input("Find by Name: (q to go back) ")
            if name == 'q':
                self.main_menu()
                return
            for s in self.book.student_list:
                if s.name.lower() == name.lower():
                    match = s
                    break
            if match is None:
                print("Could not find student named- {}".format(name))

        self.book.student_list.remove(match)
        self.book.write()

        self.main_menu()


def main():
    menu = MenuDriven()
    menu.main_menu()


if __name__ == '__main__':
    main()
