import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#Written By Jake Reddock
class database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect('example.db')

    # Written By Jake Reddock
    def query(self, sql):
        try:
            self.conn.row_factory = dict_factory
            c = self.conn.cursor()
            c.execute("""PRAGMA encoding="UTF-8";""")
            query_resource = c.execute(sql).fetchall()
            self.conn.commit()
            return database_result(self, query_resource)
        except Exception as err:
            print('Query Failed: %s\nError: %s' % (sql, str(err)))
            return False

    # Written by Jake Reddock
    def close(self):
        """Close the connection to the database
        """
        self.conn.close()

#Written By Jake Reddock
class database_result:
    def __init__(self, database, query):
        self.database = database
        self.query = query

    # Written By Jake Reddock
    def size(self):
        return len(self.query)

    # Written By Jake Reddock
    def fetch(self):
        return self.query

#Written By Jake Reddock
if __name__ == '__main__':
    db = database("")
    db.query("""
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
