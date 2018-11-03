import plotly

from src.database import sql
from src.database.class_data import ClassData

from src.strategy.graph_strategy import AbstractGraphBuilder


class BarGraphCreator(AbstractGraphBuilder):
    def __init__(self, db_name):
        self.db = sql.database(db_name)

    def initialize(self):
        self.db.query(
            "CREATE TABLE IF NOT EXISTS ClassData (classID INTEGER PRIMARY KEY AUTOINCREMENT, className "
            "TEXT, attributeCount INTEGER, methodCount INTEGER);")
        self.db.query("INSERT INTO ClassData VALUES(null,'tester', 2, 3);")

    def insert(self):
        class_data_list = []
        result = []
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

    def create(self, statistics):
        self.class_names = []
        self.class_attributes = []
        self.class_methods = []
        for class_data in statistics.get_class_data():
            self.class_names.append(class_data.class_name)
            self.class_attributes.append(class_data.attribute_count)
            self.class_methods.append(class_data.method_count)

        self.attribute_trace = plotly.graph_objs.Bar(
            x=self.class_names,
            y=self.class_attributes,
            name='Attribute Count'
        )

        self.method_trace = plotly.graph_objs.Bar(
            x=self.class_names,
            y=self.class_methods,
            name='Method Count'
        )

        data = [self.attribute_trace, self.method_trace]
        layout = plotly.graph_objs.Layout(barmode='group')

        fig = plotly.graph_objs.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename='../tmp/grouped-bar.html')