import mysql.connector


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Written by Michael Huang


class MyDatabase:
    def __init__(self, name):
        self.name = name
        self.conn = mysql.connector.connect(host='localhost',
                                            user='root',
                                            password='')

    # Written by Michael Huang

    def create_database(self):
        """
        Create a database using mysql connector
        Author: Michael Huang
        
        >>> db = MyDatabase("office")
        >>> db.create_database()
        True    
        """
        c = self.conn.cursor()
        c.execute("DROP DATABASE IF EXISTS " + self.name)
        c.execute("CREATE DATABASE " + self.name)
        c.execute("USE " + self.name)
        self.conn.commit()
        if self.name:
            return True

    # Written by Michael Huang

    def query(self, sql):
        try:
            self.conn.row_factory = dict_factory
            c = self.conn.cursor()
            c.execute("""set character_set_results='utf8';""")
            c.execute(sql)
            if c.description is None:
                # print("Setting query")
                self.conn.commit()
                return True
            else:
                # print("Fetching query")
                query_resource = c.fetchall()
                return mysql_result(self, query_resource)
        except Exception as err:
            print('Query Failed: %s\nError: %s' % (sql, str(err)))
            print("Exception raised")
            print(err)
            return False

    def close(self):
        """Close the connection to the database
        >>> db = MyDatabase("office")
        >>> db.create_database()
        True
        >>> db.conn.close()
        
        """
        self.conn.close()
        if self.conn.close():
            return True
        else:
            return False

    # Written by Michael Huang
    def validate_table(self, sql):
        """
        Checks if the table has been created and added to the database
        Author: Michael Huang
        """

        table_result = self.query(sql)
        if table_result:
            # print("Table was added")
            return True
        else:
            # print("Table was not added")
            return False

# Written By Michael Huang


class mysql_result:
    def __init__(self, mydatabase, query):
        self.mydatabase = mydatabase
        self.query = query

    def size(self):
        return len(self.query)

    def fetch(self):
        return self.query


# Written By Michael Huang
if __name__ == '__main__':
    db = MyDatabase("office")
    db.create_database()
    db.query("""
CREATE TABLE if not exists employee (
staff_number INTEGER PRIMARY KEY auto_increment,
fname VARCHAR(20),
lname VARCHAR(30),
gender CHAR(1),
birth_date DATE);""")

    db.query(
        """INSERT INTO employee VALUES (null, "Frank", "Schiller", "m", "1955-08-17")""")
    result = db.query("""SELECT fname FROM employee""").fetch()
    print(result)
    print(db.query("""SELECT * FROM employee""").size())
    for row in result:
        print(row[0])
