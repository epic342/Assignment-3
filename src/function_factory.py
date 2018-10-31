from abc import ABCMeta, abstractmethod


class FunctionFactory(metaclass=ABCMeta):
    def __init__(self, name, list_of_parameters, visibility):
        self.name = name
        self.parameters = list_of_parameters
        self.visibility = visibility

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_parameters(self):
        pass
