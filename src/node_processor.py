from src.class_factory import ClassFactory
from src.function_factory import FunctionFactory


class ClassNode(ClassFactory):
    def add_attribute(self, attribute_name, visibility):
        self.attributes.append(AttributeNode(attribute_name, visibility))

    def add_function(self, function_name, list_of_parameters, visibility):
        self.functions.append(FunctionNode(function_name,
                                           list_of_parameters, visibility))

    def add_super_class(self, super_class):
        self.super_classes.append(super_class)


class AttributeNode:
    def __init__(self, name, visibility):
        self.name = name
        self.visibility = visibility


class FunctionNode(FunctionFactory):
    def get_name(self):
        return self.name

    def get_parameters(self):
        return ",".join(self.parameters)
