import unittest

import controllers
from databases import Connection


class TestNewcomers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        conn = Connection.get_connection('test')
        cls.newcomers = controllers.get_newcomers(conn, 100)

    def verify_valid_newcomers(self):
        self.newcomers

if __name__ == '__main__':
    unittest.main()
