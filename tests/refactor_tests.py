import unittest
import os
from src.command_interpreter import CommandLine as Controller

class RefactorTest(unittest.TestCase):

    def setUp(self):
        if os.path.exists("RefactorTest.db"):
            os.remove("RefactorTest.db")

    def tearDown(self):
        if os.path.exists("RefactorTest.db"):
            os.remove("RefactorTest.db")

    def test_cmd_set_input_file_args(self):
        """
        Large Class - Test 1
        Is it still possible to set the input file using command line arguments?
        Author: Michael Huang
        """
        controller = Controller()
        controller.do_set_input_file("plants.py")
        self.assertTrue(controller.files, ["plants.py"])

    def test_cmd_copy_output_file_args(self):
        """
        Large Class - Test 2
        Is it still possible to set the input file using command line arguments?
        Author: Michael Huang
        """
        controller = Controller()
        output = controller.do_output_to_file(os.getcwd())
        self.assertEqual(output, controller.output)

    def test_cmd_change_python_files(self):
        """
        Large Class - Test 3
        Is it still possible to parse input files?
        Author: Michael Huang
        """
        controller = Controller()
        controller.do_change_python_files("plants.py")
        self.assertIsNotNone(controller.files)

if __name__ == '__main__':
    unittest.main()