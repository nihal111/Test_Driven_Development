import unittest
from bookkeeper import main
import os
import random
import io
from unittest.mock import patch, MagicMock
import sys


class TestBookkeeper(unittest.TestCase):
    def setUp(self):
        self.student = main.Student("Nihal", "9876543210", [94.3, 99.6, 84.5])
        self.s1 = main.Student("S1", "1111111111", [11, 22, 33.3])
        self.s2 = main.Student("S2", "2222222222", [77.1, 78, 13.3])
        self.s3 = main.Student("S3", "3333333333", [15, 24.2, 51.3])
        self.student_list = [self.s1, self.s2, self.s3]

    def test_student_creation(self):
        self.assertEqual(self.student.name, "Nihal")
        self.assertEqual(self.student.phone_number, "9876543210")
        self.assertEqual(self.student.marks, [94.3, 99.6, 84.5])

    def test_student_name_update(self):
        self.assertEqual(self.student.name, "Nihal")
        self.student.update_name("NEWNAME")
        self.assertEqual(self.student.name, "NEWNAME")

    def test_student_phone_number_update(self):
        self.assertEqual(self.student.phone_number, "9876543210")
        self.student.update_phone_number("1234567890")
        self.assertEqual(self.student.phone_number, "1234567890")

    def test_student_marks_update(self):
        old_marks = [94.3, 99.6, 84.5]
        self.assertEqual(self.student.marks, old_marks)
        new_marks = [70, 80, 90]
        self.student.update_marks(new_marks)
        self.assertEqual(self.student.marks, new_marks)

    def test_create_book(self):
        path = "save.txt"
        book = main.Book(path, self.student_list)
        self.assertEqual(book.student_list, self.student_list)
        self.assertEqual(book.path, path)

    def test_book_write(self):
        path = "test_{}.txt".format(random.randint(1000, 9999))
        book = main.Book(path, self.student_list)
        book.write()

        with open(path, 'r+') as f:
            content = f.readlines()

        for i in range(len(self.student_list)):
            s = self.student_list[i]
            line = "{},{},{},{},{}\n".format(
                s.name, s.phone_number, s.marks[0], s.marks[1], s.marks[2])

            self.assertEqual(line, content[i])

        os.remove(path)

    def test_book_read(self):
        path = "test_{}.txt".format(random.randint(1000, 9999))
        book = main.Book(path)

        with open(book.path, 'w+') as f:
            for s in self.student_list:
                line = "{},{},{},{},{}\n".format(
                    s.name, s.phone_number, s.marks[0], s.marks[1], s.marks[2])
                f.write(line)

        book.read()
        self.assertEqual(len(self.student_list), len(book.student_list))
        for i in range(len(self.student_list)):
            stud1 = self.student_list[i]
            stud2 = book.student_list[i]
            self.assertEqual(stud1.name, stud2.name)
            self.assertEqual(stud1.phone_number, stud2.phone_number)
            self.assertEqual(stud1.marks, stud2.marks)
        os.remove(path)

    # @patch('sys.stdout', new_callable=io.StringIO)
    # def test_main_menu_prompt(self, mock_stdout):
    #     main.main_menu()
    #     self.assertEqual(mock_stdout.getvalue(),
    #                      "1. Add\n2. Edit\n3. Delete\n\n")

    @patch('builtins.input', return_value='1')
    def test_main_menu_add(self, input):
        menu_driven = main.MenuDriven()
        menu_driven.add_screen = MagicMock()
        captured_output = io.StringIO()          # Create StringIO object
        sys.stdout = captured_output             # and redirect stdout.
        menu_driven.main_menu()
        self.assertEqual(captured_output.getvalue(),
                         "1. Add\n2. Edit\n3. Delete\nq. Quit\n\n")
        sys.stdout = sys.__stdout__              # Reset redirect.
        assert menu_driven.add_screen.called

    @patch('builtins.input', return_value='2')
    def test_main_menu_edit(self, input):
        menu_driven = main.MenuDriven()
        menu_driven.edit_screen = MagicMock()
        captured_output = io.StringIO()          # Create StringIO object
        sys.stdout = captured_output             # and redirect stdout.
        menu_driven.main_menu()
        self.assertEqual(captured_output.getvalue(),
                         "1. Add\n2. Edit\n3. Delete\nq. Quit\n\n")
        sys.stdout = sys.__stdout__              # Reset redirect.
        assert menu_driven.edit_screen.called

    @patch('builtins.input', return_value='3')
    def test_main_menu_delete(self, input):
        menu_driven = main.MenuDriven()
        menu_driven.delete_screen = MagicMock()
        captured_output = io.StringIO()          # Create StringIO object
        sys.stdout = captured_output             # and redirect stdout.
        menu_driven.main_menu()
        self.assertEqual(captured_output.getvalue(),
                         "1. Add\n2. Edit\n3. Delete\nq. Quit\n\n")
        sys.stdout = sys.__stdout__              # Reset redirect.
        self.assertTrue(menu_driven.delete_screen.called)

    @patch('builtins.input', return_value='q')
    def test_main_menu_quit(self, input):
        menu_driven = main.MenuDriven()
        captured_output = io.StringIO()          # Create StringIO object
        sys.stdout = captured_output             # and redirect stdout.

        with self.assertRaises(SystemExit) as cm:
            menu_driven.main_menu()
            self.assertEqual(cm.exception.code, 1)

        self.assertEqual(captured_output.getvalue(),
                         "1. Add\n2. Edit\n3. Delete\nq. Quit\n\n")
        sys.stdout = sys.__stdout__              # Reset redirect.

    @patch('builtins.input')
    def test_marks_input1(self, mock_get_input):
        mock_get_input.side_effect = ['14', '16a', '16', '15']
        captured_output = io.StringIO()          # Create StringIO object
        sys.stdout = captured_output             # and redirect stdout.
        main.get_marks()
        sys.stdout = sys.__stdout__              # Reset redirect.

    @patch('builtins.input')
    def test_marks_input2(self, mock_get_input):
        mock_get_input.side_effect = ['14,5', '14.5', '16', '15']
        captured_output = io.StringIO()          # Create StringIO object
        sys.stdout = captured_output             # and redirect stdout.
        main.get_marks()
        sys.stdout = sys.__stdout__              # Reset redirect.

    @patch('builtins.input')
    def test_enter_details(self, mock_get_input):
        menu_driven = main.MenuDriven()
        mock_get_input.side_effect = [
            "Nihal", "9876543210", '94.3', '99.6', '84.5']
        captured_output = io.StringIO()          # Create StringIO object
        sys.stdout = captured_output             # and redirect stdout.
        student = menu_driven.enter_details()
        sys.stdout = sys.__stdout__              # Reset redirect.

        self.assertEqual(student.name, "Nihal")
        self.assertEqual(student.phone_number, "9876543210")
        self.assertEqual(student.marks, [94.3, 99.6, 84.5])

    @patch('bookkeeper.main.MenuDriven.enter_details')
    def test_add_screen(self, mock_get_input):
        menu_driven = main.MenuDriven()
        path = "test_{}.txt".format(random.randint(1000, 9999))
        menu_driven.book.path = path
        menu_driven.main_menu = MagicMock()

        mock_get_input.return_value = self.student

        captured_output = io.StringIO()          # Create StringIO object
        sys.stdout = captured_output             # and redirect stdout.
        menu_driven.add_screen()
        sys.stdout = sys.__stdout__              # Reset redirect.

        self.assertEqual(self.student.name,
                         menu_driven.book.student_list[-1].name)
        self.assertEqual(self.student.phone_number,
                         menu_driven.book.student_list[-1].phone_number)
        self.assertEqual(self.student.marks,
                         menu_driven.book.student_list[-1].marks)

        self.assertTrue(menu_driven.main_menu.called)
        os.remove(path)

    @patch('builtins.input')
    def test_edit_screen(self, mock_get_input):
        menu_driven = main.MenuDriven()
        path = "test_{}.txt".format(random.randint(1000, 9999))
        menu_driven.book.path = path
        menu_driven.main_menu = MagicMock()

        menu_driven.book.student_list = self.student_list
        mock_get_input.side_effect = ['no match', 'S1',
                                      'Snew', '1234567890', '97', '98', '99']

        captured_output = io.StringIO()          # Create StringIO object
        sys.stdout = captured_output             # and redirect stdout.
        menu_driven.edit_screen()
        sys.stdout = sys.__stdout__              # Reset redirect.

        self.assertEqual('Snew',
                         menu_driven.book.student_list[-1].name)
        self.assertEqual('1234567890',
                         menu_driven.book.student_list[-1].phone_number)
        self.assertEqual([97, 98, 99],
                         menu_driven.book.student_list[-1].marks)

        self.assertTrue(menu_driven.main_menu.called)

        os.remove(path)

    @patch('builtins.input')
    def test_edit_screen_q(self, mock_get_input):
        menu_driven = main.MenuDriven()

        menu_driven.main_menu = MagicMock()
        menu_driven.book.student_list = self.student_list
        mock_get_input.side_effect = ['q']

        # captured_output = io.StringIO()          # Create StringIO object
        # sys.stdout = captured_output             # and redirect stdout.
        menu_driven.edit_screen()
        sys.stdout = sys.__stdout__              # Reset redirect.

        self.assertTrue(menu_driven.main_menu.called)

    @patch('builtins.input')
    def test_delete_screen(self, mock_get_input):
        menu_driven = main.MenuDriven()
        menu_driven.main_menu = MagicMock()

        path = "test_{}.txt".format(random.randint(1000, 9999))
        menu_driven.book.path = path
        menu_driven.book.student_list = self.student_list
        mock_get_input.side_effect = ['no match', 'S1']

        captured_output = io.StringIO()          # Create StringIO object
        sys.stdout = captured_output             # and redirect stdout.
        menu_driven.delete_screen()
        sys.stdout = sys.__stdout__              # Reset redirect.

        self.assertEqual(len(menu_driven.book.student_list), 2)
        self.assertTrue(menu_driven.main_menu.called)

        os.remove(path)

    @patch('builtins.input')
    def test_delete_screen_q(self, mock_get_input):
        menu_driven = main.MenuDriven()

        menu_driven.main_menu = MagicMock()
        menu_driven.book.student_list = self.student_list
        mock_get_input.side_effect = ['q']

        captured_output = io.StringIO()          # Create StringIO object
        sys.stdout = captured_output             # and redirect stdout.
        menu_driven.delete_screen()
        sys.stdout = sys.__stdout__              # Reset redirect.

        self.assertTrue(menu_driven.main_menu.called)

    @patch('bookkeeper.main.MenuDriven')
    def test_main(self, mock_menu_driven):
        mock_instance = mock_menu_driven.return_value

        main.main()

        mock_menu_driven.assert_called_with()
        mock_instance.main_menu.assert_called_with()


if __name__ == '__main__':
    unittest.main()
