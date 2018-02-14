from unittest import TestCase, main
import codecs
import os
from .search_index import SearchIndex


class TestSearchIndex(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.SI = SearchIndex()
        doc1 = "Пеппи сидела на диване и молча слушала разговор дам"
        cls.SI.create_index(doc1)

    def test_extract_alphanum_data(self):
        res = SearchIndex.extract_alphanum_data("123!")
        self.assertEqual("123", res)

    def test_create_gram_list(self):
        res = SearchIndex.create_gram_list("1234")
        self.assertListEqual(["123", "234"], res)

    def test_create_index(self):
        # assert all trigrams are contained
        self.assertEqual(26, len(self.SI.SEARCH_INDEX.keys()))

    def test_score1(self):

        score = self.SI.search_score("слушала")
        self.assertEqual(0.9473684210526316, score)


class TestLongDocument(TestCase):

    def test_long_document(self):
        with codecs.open(os.path.dirname(__file__) + "/draka.txt", "r", "utf-8") as h:
            document1 = h.read()
        SI = SearchIndex()
        SI.create_index(document1)

        score = SI.search_score("побежали в XXX ванную, XXX")
        self.assertEqual(0.4162564212328766, score)


if __name__ == '__main__':
    main()