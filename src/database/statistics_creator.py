from src.adapter.adapter_factory import AdapterFactory
from src.database import sql
from src.database.class_data import ClassData


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


if __name__ == '__main__':
    print()
