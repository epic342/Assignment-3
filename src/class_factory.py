from abc import ABCMeta, abstractmethod

class ClassFactory(metaclass=ABCMeta):

    def __init__(self, name, super_classes=None):
        self.name = name
        self.attributes = []
        self.functions = []
        if super_classes is None:
            self.super_classes = []
        else:
            self.super_classes = super_classes

    @abstractmethod
    def add_attribute(self, attribute_name, visibility):
        pass

    @abstractmethod
    def add_function(self, function_name, list_of_parameters, visibility):
        pass

    @abstractmethod
    def add_super_class(self, super_class):
        pass