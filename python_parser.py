import sys
import inspect


class ClassNode:
    def __init__(self, name, super_classes):
        self.name = name
        self.attributes = []
        self.functions = []
        self.super_classes = super_classes

    def add_attribute(self, attribute_name):
        self.attributes.append(AttributeNode(attribute_name))

    def add_function(self, function_name):
        self.functions.append(FunctionNode(function_name))


class AttributeNode:
    def __init__(self, name):
        self.name = name


class FunctionNode:
    def __init__(self, name):
        self.name = name


class FileProcessor:

    filter_out_attributes = ["__doc__", "__module__", "__dict__", "__weakref__"]

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

        # print(module.Plant.__dict__) - lets me see global variables, but not function variables
        # print(module.Plant.__init__)

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

        # create module for current file in global modules list
        if not module_name in self.modules:
            self.modules[module_name] = list()

        # create class node and append to current module
        class_node = ClassNode(name, some_class.__bases__)
        self.modules[module_name].append(class_node)

        # create list of attributes in class
        for (name, something) in inspect.getmembers(some_class()):
            if not callable(something):
                self.process_attribute(name, class_node)

        # create list of functions in class
        for (name, something) in inspect.getmembers(some_class):
            if inspect.ismethod(something) or inspect.isfunction(something):
                self.process_function(something, class_node)

    def process_function(self, some_function, class_node):
        """Functions are added to the class node with just their title"""
        print("Processing function: " + some_function.__name__)

        #print(type(some_function))
        # print("The parameters for this function are: ", inspect.getargspec(some_function))

        class_node.add_function(some_function)

    def process_attribute(self, attribute_name, class_node):
        """Attributes are added to the class node with just their name"""
        # filter out __module__, __doc__
        if attribute_name not in self.filter_out_attributes:
            print("Processing attribute: " + attribute_name)
            class_node.add_attribute(attribute_name)


if __name__ == "__main__":
    # USAGE: python_parser.py <filename or * for all>.py

    if len(sys.argv) == 1:
        print("USAGE: " + sys.argv[0] + " <pythonfiles>")
    else:
        print("STARTING PROCESSING")

        processor = FileProcessor()
        processor.process_files(sys.argv[1:])
