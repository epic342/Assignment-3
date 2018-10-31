import inspect
import os
import sys
from src.node_processor import ClassNode


##########################################
# Initial helper classes to store information while the parser
# parses the information


class FileProcessor:
    """
    Process multiple files into class objects ready to be converted into DOT
    Author: Braeden
    """
    filter_out_attributes = [
        "__doc__",
        "__module__",
        "__dict__",
        "__weakref__"]

    def __init__(self, statistics):
        self.modules = dict()
        self.statistics = statistics

    def process_files(self, file_names):
        """
        Loop through a list of files, and process each file as an individual
        Author: Braeden
        >>> fp.process_files(["plants.py"])
        1
        >>> fp.process_files(["plants.py", "controller.py"])
        2
        """
        for file in file_names:
            self.process_file(file)
        return len(self.modules)

    def process_file(self, file_name):
        # Import specified file_name and store as module
        path, file = os.path.split(file_name)
        module_name = file.replace(
            "./",
            "").replace(
            ".py",
            "").replace(
            "/",
            ".")

        # change path for import to directory of file
        sys.path.append(path)

        try:
            __import__(module_name, locals(), globals())
            self.process_module(sys.modules[module_name])
        except ImportError:
            print("A file with this name could not be found, please try again.")
        except OSError:
            print("The provided python file contains invalid syntax, "
                  "please fix the provided code before running")
        except:
            print("Query Failed: An unexpected exception")

    def process_module(self, module):
        # Find any classes that exists within this module
        for (name, something) in inspect.getmembers(module):
            if inspect.isclass(something):
                self.process_class(something)

    def process_class(self, some_class):
        # Process the found class, and store in global modules
        # Find any functions with-in the class
        name = some_class.__name__

        module_name = some_class.__module__

        # create module for current file in global modules list
        if module_name not in self.modules:
            self.modules[module_name] = list()

        super_classes = []
        super_classes_names = []

        super_classes = self.create_super_class(super_classes, super_classes_names, some_class)

        # create class node and append to current module
        class_node = ClassNode(name, super_classes)
        self.modules[module_name].append(class_node)
        self.get_class_functions(some_class, class_node)

        if self.statistics is not None:
            self.statistics.insert_class(class_node)

    def get_class_functions(self, some_class, class_node):
        # create list of functions in class
        for (name, something) in inspect.getmembers(some_class):
            if inspect.ismethod(something) or inspect.isfunction(something):
                # get the class from the functions element
                function_class = something.__qualname__.split('.')[0]

                # only add function if the current class is the same as the
                # selected functions class
                if some_class.__name__ == function_class:
                    # create list of attributes in class with constructor
                    if something.__name__ == "__init__":
                        attributes = something.__code__.co_names

                        for attribute in attributes:
                            self.process_attribute(
                                attribute, class_node, self.get_visibility_of_string(attribute))

                    self.process_function(
                        something,
                        class_node,
                        self.get_visibility_of_string(
                            something.__name__))

    @staticmethod
    def create_super_class(super_classes, super_classes_names, some_class):
        for class_object in some_class.__bases__:
            if class_object.__name__ != 'object':
                if class_object.__name__ not in super_classes_names:
                    super_classes.append(class_object)
                    super_classes_names.append(class_object.__name__)
        return super_classes

    @staticmethod
    def process_function(some_function, class_node, visibility):
        # Functions are added to the class node with just their title
        class_node.add_function(
            some_function.__name__,
            inspect.getfullargspec(some_function)[0],
            visibility)

    def process_attribute(self, attribute_name, class_node, visibility):
        # Attributes are added to the class node with just their name
        # filter out __module__, __doc__
        if attribute_name not in self.filter_out_attributes:
            class_node.add_attribute(attribute_name, visibility)

    def get_modules(self):
        return self.modules

    @staticmethod
    def get_visibility_of_string(string):
        """
        get visibility of function (public = +, protected = #, private = -)
        Author: Braeden
        >>> FileProcessor().get_visibility_of_string("test")
        '+'
        >>> FileProcessor().get_visibility_of_string("__test")
        '-'
        >>> FileProcessor().get_visibility_of_string("_test")
        '#'
        """
        visibility = "+"
        if string[:2] == "__":
            visibility = "-"
        elif string[0] == "_":
            visibility = "#"
        return visibility


if __name__ == "__main__":
    import doctest

    doctest.testmod(extraglobs={'fp': FileProcessor()})
