import unittest
import sqlcontrol

"""
>>> output_to_file E:\BCPR301 - Advanced Programming
The output to the file destination was successful.

"""


# Written By Michael Huang

class MichaelTest(unittest.TestCase):

    def test_database_connection(self):
        """
        Is the database connected?
        Author: Michael Huang
        """
        db = sqlcontrol.MyDatabase("unittest")
        self.assertIsNotNone(db.conn)
        db.close()

    def test_close_connection(self):
        """
        Is the connection to the database closed?
        Author: Michael Huang
        """
        db = sqlcontrol.MyDatabase("unittest")
        query = db.close()
        self.assertTrue(query)

    def test_database_creation(self):
        """
        Is there a database specified to be created?
        Author: Michael Huang
        """
        db = sqlcontrol.MyDatabase("unittest")
        query = db.create_database()
        self.assertTrue(query)
        db.close()

    def test_create_table(self):
        """
        Can a table be created?
        Author: Michael Huang
        """
        db = sqlcontrol.MyDatabase("unittest")
        db.create_database()
        query = db.query("""CREATE TABLE if not exists car (
                car_number INTEGER PRIMARY KEY auto_increment,
                carname VARCHAR(20));""")
        self.assertTrue(query)
        db.close()

    def test_database_insert(self):
        """
        Can data be inserted into the database?
        Author: Michael Huang
        """
        db = sqlcontrol.MyDatabase("unittest")
        db.create_database()
        query = db.query("""CREATE TABLE if not exists car (
                        car_number INTEGER PRIMARY KEY auto_increment,
                        carname VARCHAR(20));""")
        query2 = db.query("""INSERT INTO car VALUES (null, "Frank")""")
        self.assertEqual(query, query2)
        db.close()

    def test_database_select(self):
        """
        Can you select data from a table in a database?
        Author: Michael Huang
        """
        db = sqlcontrol.MyDatabase("unittest")
        db.create_database()
        query = db.query("""CREATE TABLE if not exists car (
                        car_number INTEGER PRIMARY KEY auto_increment,
                        carname VARCHAR(20));""")
        query2 = db.query("""INSERT INTO car VALUES (null, "Frank")""")
        self.assertEqual(query, query2)
        query3 = db.query("""SELECT * FROM car""").size()
        query4 = 1
        self.assertEqual(query3, query4)
        db.close()

    def test_validate_table(self):
        """
        Has the table actually been created and added?
        Author: Michael Huang
        """
        db = sqlcontrol.MyDatabase("unittest")
        db.create_database()
        query = db.validate_table("""CREATE TABLE if not exists car (
                                car_number INTEGER PRIMARY KEY auto_increment,
                                carname VARCHAR(20));""")
        query2 = True
        self.assertEqual(query, query2)
        db.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
    # import doctest
    # doctest.testmod(verbose=True)
