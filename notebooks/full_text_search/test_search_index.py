import unittest
from .search_index import SearchIndex

doc1 = "Пеппи сидела на диване и молча слушала разговор дам"


class TestSearchIndex(unittest.TestCase):
    def setUp(self):
        self.SI = SearchIndex()

    def test_extract_alphanum_data(self):
        res = SearchIndex.extract_alphanum_data("123!")
        self.assertEqual(res, "123")

    def test_create_gram_list(self):
        res = SearchIndex.create_gram_list("1234")
        self.assertListEqual(res, ["123", "234"])

    def test_score1(self):
        self.SI.create_index(doc1)

        # In[299]:

        score = self.SI.search_score("слушала")
        self.assertEqual(score, 0.36129032258064514)

    if __name__ == '__main__':
        unittest.main()