import plotly

from src.database import sql
from src.adapter.adapter_factory import AdapterFactory
from src.database.class_data import ClassData

# By Jake Reddock

class StatisticsCreator:
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
            node_creator = AdapterFactory(class_node)
            self.db.query("INSERT INTO ClassData VALUES(null, '{}', {}, {})".format(
                          node_creator.get_class_name(),
                          node_creator.get_class_attributes(),
                          node_creator.get_class_functions()))
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
        plotly.offline.plot(fig, filename='../tmp/grouped-bar.html')


if __name__ == '__main__':
    print()
