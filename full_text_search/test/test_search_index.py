from unittest import TestCase, main
import codecs
import os
from ..search_index import SearchIndex


class TestSearchIndexAddToIndex(TestCase):
    @classmethod
    def setUp(cls):
        cls.si = SearchIndex()
        cls.si._add_to_index(0, ['xxx'])
        cls.si._add_to_index(1, ['yyy'])

    def test_add_to_index(self):
        index_exp = {
            ("xxx", 0): [0],
            ("yyy", 1): [0],
        }
        self.assertDictEqual(index_exp, self.si.INDEX)


class TestStaticFunctions(TestCase):

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

    def test_gramify(self):
        term = "1234 5678"
        expected = ["123", "234", "567", "678"]
        self.assertListEqual(expected, SearchIndex.gramify(term))


class TestSearch(TestCase):

    def test_score1(self):
        si = SearchIndex()
        si.add_to_index("слушала")
        score = si.search("слушала")
        self.assertEqual({
            '1e8b2604f23d83a1597cfb316706b215': 1.0
        }, score.value())

    def test_score_lt1(self):
        si = SearchIndex()
        si.add_to_index("слушала")
        score = si.search("слушали")
        self.assertEqual({
            '1e8b2604f23d83a1597cfb316706b215': 0.8
        }, score.value())

    def test_score_match_in_between_doc(self):
        si = SearchIndex()
        si.add_to_index("она слушала")
        score = si.search("слушала")
        self.assertEqual({
            'ce26cffa3faf2019c733f5f4c7caf074': 1.0
        }, score.value())


class TestLongDocument(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.si = SearchIndex()
        with codecs.open(os.path.dirname(__file__) + "/data/draka.txt", "r", "utf-8") as h:
            doc1 = h.read()
        cls.si.add_to_index(doc1)

    def test_long_document(self):
        score = self.si.search("побежали в XXX ванную, XXX")
        self.assertEqual({
            '74c4f720094c291f90caafcb77118f1e': 0.8332798459563543
        }, score.value())

    def test_long_document_full_match(self):
        score = self.si.search("побежали в ванную, ")
        self.assertEqual({
            '74c4f720094c291f90caafcb77118f1e': 0.9999999999999999
        }, score.value())

    def test_long_document_no_match(self):
        score = self.si.search("XXXXXX")
        self.assertEqual({}, score.value())


class TestTwoDocs(TestCase):

    @classmethod
    def setUp(cls):
        cls.si = SearchIndex()
        cls.si.add_to_index("Пеппи сидела на диване и молча слушала разговор дам")
        cls.si.add_to_index("Дорогие мои, мне так досадно: я нашла две такие чудесные вещи")

    def test_search(self):
        scores = self.si.search("досадно")
        self.assertEqual({
            '8d4e5b9a35e6679f56c2a33f2c0e1018': 1.0,
        }, scores.value())



if __name__ == '__main__':
    main()
