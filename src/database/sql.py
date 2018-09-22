import sqlite3


class SQLError(Exception):
    def __init__(self, error_message):
        self.error_message = error_message

    def __str__(self):
        return "Query Failed: %s" % self.error_message


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Written By Jake Reddock


class database:
    """
    Database object containing attribute and functions
    Author: Jake

    >>> db = database("DocTest")
    >>> db.db_name
    'DocTest'
    >>> db.query('CREATE TABLE IF NOT EXISTS TestTable (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT)').fetch()
    []
    >>> db.query("INSERT INTO TestTable VALUES(NULL,'TestName')").fetch()
    []
    >>> db.query('SELECT data FROM TestTable WHERE id=1').fetch()[0]['data']
    'TestName'
    >>> db.query('SELECT data FROM TestTable WHERE id=1').size()
    1
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name + '.db')

    # Written By Jake Reddock
    def query(self, sql):
        try:
            self.conn.row_factory = dict_factory
            c = self.conn.cursor()
            c.execute("""PRAGMA encoding="UTF-8";""")
            query_resource = c.execute(sql).fetchall()
            self.conn.commit()
            return database_result(self, query_resource)
        except sqlite3.OperationalError as err:
            raise SQLError(err)
        except:
            print("Query Failed: An unexpected exception")

    # Written by Jake Reddock
    def close(self):
        """
        Close the connection to the database
        """
        self.conn.close()

# Written By Jake Reddock


class database_result:
    """
    Database Result object containing attributes and functions
    Author: Jake

    >>> database = database("DocTest")
    >>> query = database.conn.cursor().execute('SELECT data FROM TestTable WHERE id=1').fetchall()
    >>> database_result(database, query).size()
    1
    >>> query = database.conn.cursor().execute('SELECT data FROM TestTable WHERE id=1').fetchall()
    >>> database_result(database, query).fetch()[0][0]
    'TestName'
    """
    def __init__(self, database, query):
        self.database = database
        self.query = query

    # Written By Jake Reddock
    def size(self):
        return len(self.query)

    # Written By Jake Reddock
    def fetch(self):
        return self.query


# Written By Jake Reddock
if __name__ == '__main__':
    db = database("")
    db.query, db.create_table("""
CREATE TABLE if not exists employee (
staff_number INTEGER PRIMARY KEY,
fname VARCHAR(20),
lname VARCHAR(30),
gender CHAR(1),
birth_date DATE);""")

    db.query("""INSERT INTO employee
    VALUES (NULL, "Frank", "Schiller", "m", "1955-08-17")""")
    result = db.query("""SELECT * FROM employee""").fetch()
    print(db.query("""SELECT * FROM employee""").size())
    for row in result:
        print(row["fname"])
