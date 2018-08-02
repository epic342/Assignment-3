import sys
import inspect


def log(string):
    sys.stderr.write("LOG: " + string + "\n")


class ClassNode:
    def __init__(self, name, super_classes):
        self.name = name
        self.attributes = []
        self.functions = []
        self.super_classes = super_classes

    def add_attribute(self, attribute_name):
        self.attributes.append(AttributeNode(attribute_name))

    def add_function(self, function_name, list_of_parameters):
        self.functions.append(FunctionNode(function_name, list_of_parameters))


class AttributeNode:
    def __init__(self, name):
        self.name = name


class FunctionNode:
    def __init__(self, name, list_of_parameters):
        self.name = name
        self.parameters = list_of_parameters


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

        #print("Processing " + file_name)

        module_name = file_name.replace("./", "").replace(".py", "").replace("/", ".")

        __import__(module_name, locals(), globals())

        self.process_module(sys.modules[module_name])

    def process_module(self, module):
        """Find any classes that exists within this module"""
        #print("Processing module " + str(module))

        for (name, something) in inspect.getmembers(module):
            if inspect.isclass(something):
                self.process_class(something)
            else:
                pass

    def process_class(self, some_class):
        """Process the found class, and store in global modules
        Find any functions with-in the class"""
        name = some_class.__name__

        #print("Processing class: " + name + " in module " + some_class.__module__)

        module_name = some_class.__module__

        # create module for current file in global modules list
        if not module_name in self.modules:
            self.modules[module_name] = list()

        # strip bases
        super_classes = []
        super_classes_names = []

        for x in some_class.__bases__:
            if x.__name__ != 'object':
                if x.__name__ not in super_classes_names:
                    super_classes.append(x)
                    super_classes_names.append(x.__name__)
        
        # create class node and append to current module
        class_node = ClassNode(name, super_classes)
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
        #print("Processing function: " + some_function.__name__, " - The parameters are:", inspect.getargspec(some_function)[0])
        class_node.add_function(some_function, inspect.getfullargspec(some_function)[0])

    def process_attribute(self, attribute_name, class_node):
        """Attributes are added to the class node with just their name"""
        # filter out __module__, __doc__
        if attribute_name not in self.filter_out_attributes:
            #print("Processing attribute: " + attribute_name)
            class_node.add_attribute(attribute_name)

    def output_to_dot(self, out):
        """Output as UML class diagram using DOT (graphviz)"""
        def line(s):
            return out.write(s + "\n")

        def class_name_to_dot(name):
            return name

        def write_row(out, method):
            out.write(method + "\l")

        out.write(
            """
            digraph G {
                rankdir=BT
                node [
                    fontname = "Sans Not-Rotated 8"
                    fontsize = 8
                    shape = "record"
                ]
                edge [
                    fontname = "Sans Not-Rotated 8"
                    fontsize = 8
                ]
            """
        )

        for (name, module) in self.modules.items():
            if len(module) > 1:
                line("subgraph {")

            for c in module:
                line(class_name_to_dot(c.name) + " [")

                # Class Title
                out.write("label = \"{" + c.name)

                out.write("}\"\n")

                line("]")

            if len(module) > 1:
                line("}")

        out.write("""
            edge [
                arrowhead = "empty"
            ]
        """)

        for module in self.modules.values():
            for c in module:
                for parent in c.super_classes:
                    line(class_name_to_dot(c.name) + " -> " +
                         class_name_to_dot(parent.__name__))

        line("}")


if __name__ == "__main__":
    # USAGE: python_parser.py <filename or * for all>.py
    # FOR OUTPUTTING DOT: | dot -T png -o output.png

    if len(sys.argv) == 1:
        print("USAGE: " + sys.argv[0] + " <pythonfiles>")
    else:
        #print("STARTING PROCESSING")

        processor = FileProcessor()
        processor.process_files(sys.argv[1:])
        processor.output_to_dot(sys.stdout)
