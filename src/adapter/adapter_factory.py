from src.database.class_data import ClassData


class AdapterFactory(ClassData):

    def __init__(self, class_node):
        self.node_creator = class_node

    def get_class_name(self):
        return self.node_creator.get_class_name()

    def get_class_attributes(self):
        return len(self.node_creator.get_class_attributes())

    def get_class_functions(self):
        return len(self.node_creator.get_class_functions())