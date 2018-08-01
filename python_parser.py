import sys
import inspect


class ClassNode:
    def __init__(self, name, super_classes):
        self.name = name
        self.attributes = []
        self.functions = []
        self.super_classes = super_classes

    def add_attribute(self, attribute):
        self.attributes.append(attribute)

    def add_function(self, function):
        self.functions.append(function)
        

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

    def process_module(self, module):
        """Find any classes that exists within this module"""
        print("Processing module " + str(module))

        for (name, something) in inspect.getmembers(module):
            if inspect.isclass(something):
                self.process_class(something)
            else:
                pass

    def process_class(self, some_class):
        """Process the found class, and store in global modules
        Find any functions with-in the class"""
        name = some_class.__name__

        print("Processing class: " + name + " in module " + some_class.__module__)

        module_name = some_class.__module__

        if not module_name in self.modules:
            self.modules[module_name] = list()

        class_node = ClassNode(name, some_class.__bases__)
        self.modules[module_name].append(class_node)


if __name__ == "__main__":
    # USAGE: python_parser.py <filename or * for all>.py

    if len(sys.argv) == 1:
        print("USAGE: " + sys.argv[0] + " <pythonfiles>")
    else:
        print("STARTING PROCESSING FILES")

        processor = FileProcessor()
        processor.process_files(sys.argv[1:])
