import unittest
import model
import os


class ModelTestCase(unittest.TestCase):
    """
    Tests for 'model.py'
    """

    individual_file_upload = ["E:\Dropbox\ARA\2018, July, Semester Two\Advanced Programming\Assignment1-MVC\plants.py"]

    def test_individual_file_processed(self):
        """
        Is individual module created after processing of file?
        """
        file_processor = model.FileProcessor()
        modules = file_processor.process_files(self.individual_file_upload)

        self.assertTrue(len(modules) == 1)


if __name__ == '__main__':
    unittest.main()
