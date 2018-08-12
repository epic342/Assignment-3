import unittest
import model
import python_controller
import os


class ModelTestCase(unittest.TestCase):
    """
    Tests for 'model.py'
    """

    individual_file_upload = ["E:\Dropbox\ARA\2018, July, Semester Two\Advanced Programming\Assignment1-MVC\plants.py"]

    """
    Braedens test cases
    """

    def test_individual_file_processed(self):
        """
        Is individual module created after processing of file?
        """
        file_processor = model.FileProcessor()
        modules = file_processor.process_files(self.individual_file_upload)

        self.assertTrue(len(modules) == 1)

    def test_class_name(self):
        """
        Checks plants.py class names have been appended correctly
        """
        file_processor = model.FileProcessor()
        modules = file_processor.process_files(self.individual_file_upload)

        self.assertTrue(modules['plants'][0].name is 'Orchid')

    def test_parser(self):
        """
        Checks if creation of UML diagram and output to DOT file works
        """
        ctrl = python_controller.Controller

        self.assertTrue(ctrl.run_parser(self.individual_file_upload, False, False) is True)

    def test_output_to_png(self):
        """
        Checks if creation of UML diagram and output to PNG file works
        """
        ctrl = python_controller.Controller
        self.assertTrue(ctrl.do_output_to_png(None) is 0)

    def test_file_change(self):
        """
        Checks if files that are stored as system
        arguments can be changed by function
        """
        ctrl = python_controller.Controller
        ctrl.do_change_python_files(ctrl, "file_one.py file_two.py")

        self.assertTrue(ctrl.args[0] == "file_one.py")


if __name__ == '__main__':
    unittest.main()
