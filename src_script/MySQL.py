import MySQLdb
class Database(object):
    def __init__(self, host='localhost', username='root', password='', db=''):
        self.connection = MySQLdb.connect(host, username, password, db)
        self.cursor = self.connection.cursor()

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print 'success!!'
            return True
        except:
            self.connection.rollback()
            print 'duplicate!!'
            return False

    def query(self, query):
        cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        return cursor.fetchall()

    def __del__(self):
        self.connection.close()