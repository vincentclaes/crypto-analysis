import abc
import sqlite3
from sqlite3 import Error


class Connection(object):
    __metaclass__ = abc.ABCMeta

    @staticmethod
    def get_connection(db):
        if 'sqlite' == db.lower():
            return ConnectionSQLite.create_connection("/Users/vincent/Workspace/coinmarketcap_data/coinmarketcap_data.db")


    @abc.abstractmethod
    def create_connection(self):
        pass


class ConnectionSQLite(Connection):
    @staticmethod
    def create_connection(db_file):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return None

