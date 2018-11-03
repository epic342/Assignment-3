class ClassData:
    def __init__(self, class_name, attribute_count, method_count):
        self.class_name = class_name
        self.attribute_count = attribute_count
        self.method_count = method_count

    def get_class_name(self):
        return self.class_name

    def get_class_attributes(self):
        return self.attribute_count

    def get_class_functions(self):
        return self.method_count