import unittest
from unittest import mock
import builtins
import os

from pathlib import Path
import src.model as model

from src.command_interpreter import Controller
from src.database.statistics_creator import StatisticsCreator


class RefactorTest(unittest.TestCase):
    one_file = ["../tmp/plants.py"]
    multiple_files = ["../tmp/plants.py", "../src/model.py"]

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

    """
    Bad Smell 3 - Long Method
    Testing the code to see if it will still work after dealing with long methods.
    """

    def test_process_one_file(self):
        """
        Long Method - Test 1
        Can the model still process a single file?
        Author: Michael Huang
        """
        expected = 1
        statistics = StatisticsCreator("MyRefactor")
        statistics.create_tables()
        file_processor = model.FileProcessor(statistics)
        processor = file_processor.process_files(self.one_file)
        output = processor
        self.assertEqual(expected, output)

    def test_process_multiple_files(self):
        """
        Long Method - Test 2
        Can the model still process multiple files?
        Author: Michael Huang
        """
        expected = 3
        statistics = StatisticsCreator("MyRefactor")
        statistics.create_tables()
        file_processor = model.FileProcessor(statistics)
        processor = file_processor.process_files(self.multiple_files)
        output = processor
        self.assertEqual(expected, output)

    def test_set_input_file(self):
        """
        Long Method - Test 3
        Is it still possible to set the input file after fixing long method?
        Author: Michael Huang
        """
        controller = Controller()
        test = mock.MagicMock(name='input')
        test.side_effect = ['set_input_file plants.py', 'quit']
        builtins.input = test
        controller.run_console()
        output = controller.files
        self.assertIsNotNone(output)

if __name__ == '__main__':
    unittest.main(verbosity=2)
