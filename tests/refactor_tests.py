import unittest
from unittest import mock
import builtins
import os

from pathlib import Path

from src.command_interpreter import Controller


class RefactorTest(unittest.TestCase):
    def setUp(self):
        if os.path.exists("RefactorTest.db"):
            os.remove("RefactorTest.db")

    def tearDown(self):
        if os.path.exists("RefactorTest.db"):
            os.remove("RefactorTest.db")

    """
    Bad Smell 1 - Large Class
    Testing the code against the new structure
    """

    def test_cmd_set_input_file_args(self):
        """
        Large Class - Test 1
        Is it still possible to set the input file using command line arguments?
        Author: Michael Huang
        """
        controller = Controller()
        test = mock.MagicMock(name='input')
        test.side_effect = ['set_input_file', 'quit']
        builtins.input = test
        controller.run_console()
        output = controller.files
        self.assertIsNotNone(output)

    def test_cmd_copy_output_file_args(self):
        """
        Large Class - Test 2
        Is it still possible to set the output file location using command line arguments?
        Author: Michael Huang
        """
        controller = Controller()
        test = mock.MagicMock(name='input')
        test.side_effect = ['output_to_file E:\BCPR301 - Advanced Programming', 'quit']
        builtins.input = test
        controller.run_console()
        output = Path('E:\BCPR301 - Advanced Programming\class.png').exists()
        self.assertTrue(output)

    def test_cmd_create_statistics(self):
        """
        Large Class - Test 3
        Is it still possible to create statistics?
        """
        controller = Controller()
        test = mock.MagicMock(name='input')
        test.side_effect = ['enable_statistics', 'quit']
        builtins.input = test
        controller.run_console()
        output = controller.statistics
        self.assertIsNotNone(output)

    def test_cmd_change_python_files(self):
        """
        Large Class - Test 4
        Is it still possible to parse input files?
        Author: Michael Huang
        """
        controller = Controller()
        test = mock.MagicMock(name='input')
        test.side_effect = ['change_python_files plants.py', 'quit']
        builtins.input = test
        controller.run_console()
        output = controller.files
        self.assertIsNotNone(output)

    """
    Bad Smell 2 - Duplicate Code
    Re-testing the code after fixing the duplicate code.
    """

    def test_cmd_set_input_file(self):
        """
        Duplicate Code - Test 1
        Is it still possible to set the input file using command line arguments after fixing duplicate code?
        Author: Michael Huang
        """
        controller = Controller()
        test = mock.MagicMock(name='input')
        test.side_effect = ['set_input_file', 'quit']
        builtins.input = test
        controller.run_console()
        output = controller.files
        self.assertIsNotNone(output)

    def test_cmd_copy_output_file(self):
        """
        Duplicate Code - Test 2
        Is it still possible to set the output file location using command line arguments after fixing duplicate code?
        Author: Michael Huang
        """
        controller = Controller()
        test = mock.MagicMock(name='input')
        test.side_effect = ['output_to_file E:\BCPR301 - Advanced Programming', 'quit']
        builtins.input = test
        controller.run_console()
        output = Path('E:\BCPR301 - Advanced Programming\class.png').exists()
        self.assertTrue(output)

    def test_cmd_enable_statistics(self):
        """
        Duplicate Code - Test 3
        Is it still possible to create statistics after fixing duplicate code?
        """
        controller = Controller()
        test = mock.MagicMock(name='input')
        test.side_effect = ['enable_statistics', 'quit']
        builtins.input = test
        controller.run_console()
        output = controller.statistics
        self.assertIsNotNone(output)


if __name__ == '__main__':
    unittest.main(verbosity=2)
