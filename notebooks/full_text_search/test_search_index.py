import unittest
from .search_index import SearchIndex

doc1 = "Пеппи сидела на диване и молча слушала разговор дам"


class TestSearchIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.SI = SearchIndex()
        cls.SI.create_index(doc1)

    def test_extract_alphanum_data(self):
        res = SearchIndex.extract_alphanum_data("123!")
        self.assertEqual(res, "123")

    def test_create_gram_list(self):
        res = SearchIndex.create_gram_list("1234")
        self.assertListEqual(res, ["123", "234"])

    def test_create_index(self):
        # assert all trigrams are contained
        self.assertEqual(len(self.SI.SEARCH_INDEX.keys()), 26)

    def test_score1(self):
        self.SI.create_index(doc1)

        # In[299]:

        score = self.SI.search_score("слушала")
        self.assertEqual(score, 0.9800000000000001)

    if __name__ == '__main__':
        unittest.main()