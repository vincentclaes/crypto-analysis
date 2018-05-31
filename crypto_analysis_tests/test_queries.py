import unittest

from crypto_analysis.databases import Connection
from crypto_analysis.databases import queries


class TestQueries(unittest.TestCase):
    MAX_UUID = 1526408353

    @classmethod
    def setUpClass(cls):
        cls.conn = Connection.get_connection('test')

    def test_verify_valid_newcomers(self):
        uuids = queries.get_uuids(self.conn)
        self.assertEqual(TestQueries.MAX_UUID, uuids[0])

    def test_get_data_for_uuid(self):
        df = queries.get_data_for_uuid(self.conn, TestQueries.MAX_UUID, 100)
        self.assertEqual(TestQueries.MAX_UUID, df["uuid"].loc[0])
        self.assertEqual(df.shape[0], 100)

    def test_get_unique_ids_below_uuid(self):
        df = queries.get_unique_ids_below_uuid(self.conn, TestQueries.MAX_UUID, 100)
        self.assertEqual(df.shape[0], 145)


if __name__ == '__main__':
    unittest.main()
