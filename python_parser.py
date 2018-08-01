import sys
import inspect

class FileProcessor:

    def __init__(self):
        self.modules = dict()

    def process_files(self, file_names):
        """Loop through a list of files, and process each file as an individual"""
        for file in file_names:
            self.process_file(file)

    def process_file(self, file_name):
        """Import specified file_name and store as module"""

        print("Processing " + file_name)

        module_name = file_name.replace("./", "").replace(".py", "").replace("/", ".")

        __import__(module_name, locals(), globals())

        self.process_module(sys.modules[module_name])


if __name__ == "__main__":
    # USAGE: python_parser.py <filename or * for all>.py

    if len(sys.argv) == 1:
        print("USAGE: " + sys.argv[0] + " <pythonfiles>")
    else:
        print("STARTING PROCESSING FILES")

        processor = FileProcessor()
        processor.process_files(sys.argv[1:])
