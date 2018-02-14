from unittest import TestCase, main
import codecs
import os
from .search_index import SearchIndex


class TestSearchIndex(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.si = SearchIndex()
        doc1 = "Пеппи сидела на диване и молча слушала разговор дам"

        cls.si.create_index(cls.si.gramify(doc1))

    def test_extract_alphanum_data(self):
        res = SearchIndex._eliminate_punctuation("123!")
        self.assertEqual("123", res)

    def test_create_gram_list(self):
        res = SearchIndex._ngram_list(["1234"])
        self.assertListEqual(["123", "234"], res)

    def test_create_gram_list1(self):
        res = SearchIndex._ngram_list(["1234", "5678"])
        expected = ["123", "234", "567", "678"]
        self.assertListEqual(expected, res)

    def test_create_index(self):
        # assert all trigrams are contained
        self.assertEqual(26, len(self.si.SEARCH_INDEX.keys()))

    def test_gramify(self):
        term = "1234 5678"
        expected = ["123", "234", "567", "678"]
        self.assertListEqual(expected, SearchIndex.gramify(term))

    def test_score1(self):
        term_ngrams = SearchIndex.gramify("слушала")
        score = self.si.search_score(term_ngrams)
        self.assertEqual(1.0, score)


class TestLongDocument(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.si = SearchIndex()
        with codecs.open(os.path.dirname(__file__) + "/draka.txt", "r", "utf-8") as h:
            doc1 = h.read()
        cls.si.create_index(cls.si.gramify(doc1))

    def test_long_document(self):

        term_ngrams = SearchIndex.gramify("побежали в XXX ванную, XXX")
        score = self.si.search_score(term_ngrams)
        self.assertEqual(0.8332798373722784, score)

    def test_long_document_full_match(self):

        term_ngrams = SearchIndex.gramify("побежали в ванную, ")
        score = self.si.search_score(term_ngrams)
        self.assertEqual(1.0, score)

    def test_long_document_no_match(self):

        term_ngrams = SearchIndex.gramify("XXXXXX")
        score = self.si.search_score(term_ngrams)
        self.assertEqual(0.0, score)


if __name__ == '__main__':
    main()