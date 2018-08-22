import unittest
import sql
from statistics_creator import ClassData, StatisticsCreator
from model import ClassNode
from python_controller import Controller
import os


class ModelTestCase(unittest.TestCase):
    """
    Tests for 'sql.py'
    """

    def setUp(self):
        if os.path.exists("UnitTest.db"):
            os.remove("UnitTest.db")

    def tearDown(self):
        if os.path.exists("UnitTest.db"):
            os.remove("UnitTest.db")

    def test_database_creation(self):
        """
        Is the database connection being established?
        Author: Jake
        """
        db = sql.database("UnitTest")

        self.assertIsNotNone(db.conn)

    def test_database_query_table_create(self):
        """
        Is the table being created?
        Author: Jake
        """
        db = sql.database("UnitTest")
        query = db.query("""CREATE TABLE IF NOT EXISTS TestTable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT)""")

        self.assertTrue(query)

    def test_database_query_insert_data(self):
        """
        Is the data being inserted into the table?
        Author: Jake
        """
        db = sql.database("UnitTest")

        db.query("""CREATE TABLE IF NOT EXISTS TestTable (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT)""")

        query = db.query("""INSERT INTO TestTable VALUES(NULL, 'TestData')""")

        self.assertTrue(query)

    def test_database_query_fetch_data(self):
        """
        Can the data be fetched from the table?
         Author: Jake
        """
        db = sql.database("UnitTest")

        db.query("""CREATE TABLE IF NOT EXISTS TestTable (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        data TEXT)""")

        db.query("""INSERT INTO TestTable VALUES(NULL, 'TestData')""")

        query = db.query("""SELECT data FROM TestTable""")

        self.assertTrue(query)

    def test_database_get_data_from_query(self):
        """
        Can data be obtained from the query result
        Author: Jake
        """
        db = sql.database("UnitTest")

        db.query("""CREATE TABLE IF NOT EXISTS TestTable (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                data TEXT)""")

        db.query("""INSERT INTO TestTable VALUES(NULL, 'TestData')""")

        query = db.query("""SELECT data FROM TestTable WHERE id=1""")

        self.assertEqual(query.fetch()[0]['data'], "TestData")

    def test_database_get_size_query_result(self):
        """
        Can the count of items returned be gathered?
        Author: Jake
        """
        db = sql.database("UnitTest")

        db.query("""CREATE TABLE IF NOT EXISTS TestTable (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                data TEXT)""")

        db.query("""INSERT INTO TestTable VALUES(NULL, 'TestData')""")

        query = db.query("""SELECT data FROM TestTable WHERE id=1""")

        self.assertEqual(query.size(), 1)

    def test_database_exception(self):
        """
        Will an SQLError be thrown when a bad query is entered?
        Author: Jake
        """
        db = sql.database("UnitTest")
        
        with self.assertRaises(sql.SQLError):
            db.query("""SELECT * FROM UnknownTable""")

    """
    Tests for 'statistics_creator.py'
    """

    def test_statistics_creator(self):
        """
        Is the database being created when the class is created?
        Author: Jake
        """
        statistics = StatisticsCreator("UnitTest")
        
        self.assertIsNotNone(statistics.db.conn)

    def test_statistics_creator_classdata(self):
        """
        Can a ClassData object be created with correct data?
        Author: Jake
        """
        classdata = ClassData("TestName", 1, 2)

        self.assertEqual(classdata.class_name, "TestName")
        self.assertEqual(classdata.attribute_count, 1)
        self.assertEqual(classdata.method_count, 2)

    def test_statistics_creator_create_tables(self):
        """
        Is the table needed for storing data being created?
        Author: Jake
        """
        statistics = StatisticsCreator("UnitTest")
        statistics.create_tables()

        self.assertEqual(statistics.db.query("""SELECT name FROM sqlite_master WHERE type='table' AND 
        name='ClassData';""").fetch()[0]['name'], "ClassData")

    def test_statistics_creator_insert_class(self):
        """
        Can class data be inserted into the database?
        Author: Jake
        """
        classnode = ClassNode("TestName")
        classnode.add_attribute("AttributeOne", "+")
        classnode.add_function("FunctionOne", "AParameter", "+")

        statistics = StatisticsCreator("UnitTest")
        statistics.create_tables()
        statistics.insert_class(classnode)
        result = statistics.db.query("""SELECT className FROM ClassData WHERE className='TestName'""")

        self.assertEqual(result.fetch()[0]['className'], "TestName")

    def test_statistics_creator_retrieve_class(self):
        """
        Can class data be fetched from the database?
        Author: Jake
        """
        classnode = ClassNode("TestName")
        classnode.add_attribute("AttributeOne", "+")
        classnode.add_function("FunctionOne", "AParameter", "+")

        statistics = StatisticsCreator("UnitTest")
        statistics.create_tables()
        statistics.insert_class(classnode)

        self.assertEqual(statistics.get_class_data()[0].class_name, 'TestName')

    """
    Tests for 'python_controller.py'
    """

    def test_cmd_enable_statistics(self):
        """
        Is statisitcs collection enabled when the enable_statistics command is called?
        Author: Jake
        """
        controller = Controller()
        controller.do_enable_statistics("")

        self.assertIsNotNone(controller.statistics)

    def test_cmd_set_input_file(self):
        """
        Can you select a file from a file selector gui?
        Author: Jake
        """
        controller = Controller()
        controller.do_set_input_file("")

        self.assertIsNotNone(controller.files)

    def test_cmd_set_input_file_args(self):
        """
        Can you select a file from command arguments?
        Author: Jake
        """
        controller = Controller()
        controller.do_set_input_file("plants.py")

        self.assertEqual(controller.files, ["plants.py"])


if __name__ == '__main__':
    unittest.main()
