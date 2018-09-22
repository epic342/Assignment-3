import sql
import plotly


# By Jake Reddock
class ClassData:
    """
    Class Data object containing attributes
    Author: Jake

    >>> ClassData("TestClass",1,1).class_name
    'TestClass'
    >>> ClassData("TestClass",1,1).attribute_count
    1
    >>> ClassData("TestClass",1,1).method_count
    1
    """
    def __init__(self, class_name, attribute_count, method_count):
        self.class_name = class_name
        self.attribute_count = attribute_count
        self.method_count = method_count


# By Jake Reddock
class StatisticsCreator:
    """
    Statistics object containing attributes and functions
    Author: Jake

    >>> StatisticsCreator("DocTest").db.conn is not None
    True
    >>> statistics = StatisticsCreator("DocTest")
    >>> statistics.create_tables()
    >>> from model import ClassNode
    >>> classnode = ClassNode("TestName")
    >>> classnode.add_attribute("AttributeOne","+")
    >>> classnode.add_function("MethodOne","ParameterOne","+")
    >>> statistics.insert_class(classnode)
    >>> statistics.get_class_data()[0].class_name
    'TestName'
    """
    def __init__(self, db_name):
        self.db = sql.database(db_name)

    def create_tables(self):
        try:
            self.db.query(
                "CREATE TABLE IF NOT EXISTS ClassData (classID INTEGER PRIMARY KEY AUTOINCREMENT, className "
                "TEXT, attributeCount INTEGER, methodCount INTEGER);")
        except sql.SQLError as e:
            print(e)

    def insert_class(self, class_node):
        try:
            self.db.query("INSERT INTO ClassData VALUES(null,'" +
                          class_node.name + "'," +
                          str(len(class_node.attributes)) + "," +
                          str(len(class_node.functions)) + ");")
        except sql.SQLError as e:
            print(e)

    def get_class_data(self):
        class_data_list = []
        try:
            result = self.db.query(
                "SELECT className,attributeCount,methodCount from ClassData").fetch()
        except sql.SQLError as e:
            print(e)
        for row in result:
            class_name = row['className']
            attribute_count = row['attributeCount']
            method_count = row['methodCount']
            class_data_list.append(
                ClassData(
                    class_name,
                    attribute_count,
                    method_count))
        return class_data_list

    def show_graph_data(self):
        class_names = []
        class_attributes = []
        class_methods = []
        for class_data in self.get_class_data():
            class_names.append(class_data.class_name)
            class_attributes.append(class_data.attribute_count)
            class_methods.append(class_data.method_count)

        attribute_trace = plotly.graph_objs.Bar(
            x=class_names,
            y=class_attributes,
            name='Attribute Count'
        )

        method_trace = plotly.graph_objs.Bar(
            x=class_names,
            y=class_methods,
            name='Method Count'
        )

        data = [attribute_trace, method_trace]
        layout = plotly.graph_objs.Layout(barmode='group')

        fig = plotly.graph_objs.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename='grouped-bar.html')


if __name__ == '__main__':
    print()
