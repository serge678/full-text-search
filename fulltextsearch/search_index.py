from .score import Score
from hashlib import md5
import sys


class SearchIndex:
    CHARS_IN_GRAM = 3

    def __init__(self):

        """
        The search index is a dictionary of <ngram>_<doc> as keys
        and lists of occurrences.
        Structure of INDEX:
        {
            <ngram0>_<doc0>: [0, 24],
            <ngram0>_<doc1>: [13],
            ...
        }

        Structure of NGRAMS_2_DOCS:
        {
            <ngram0>: {
                <doc0>: no matter,
                <doc1>: no matter
                ...
                }
            ...
        }
        Structure of DOCS_LENGTHS:
        {
            <doc0>: length of doc0 in ngrams
            ....
        }
        """
        self.INDEX = dict()
        self.NGRAMS_2_DOCS = dict()
        self.DOCS_LENGTHS = dict()
        self.NUMBER_DOCS = 0   # Number of docs

    @staticmethod
    def _eliminate_punctuation(data):
        result = ""
        punctuation = ".,:-'\"?!<>()[]&"
        for letter in data:
            if letter not in punctuation:
                result += letter
        return result

    @classmethod
    def _ngram_list(cls, words):
        """
        Returns list of n-grams. Words with length < n are eliminated.

        :param words: list of words
        :return:
        """
        result = list()

        for word in words:
            for i in range(0, len(word) - cls.CHARS_IN_GRAM + 1):
                result.append(word[i:i + cls.CHARS_IN_GRAM])

        return result

    @staticmethod
    def gramify(data):
        """
        Takes a string (a whole document or a search term) and prepares
        it for search index / searching. It does the following:
            - eliminate punctuation
            - lowers all letters
            - splits into words
            - creates ngrams for each word
        The result is a list of ngrams

        :param data: data string
        :return: list of ngrams
        """
        data = SearchIndex._eliminate_punctuation(data)
        data = data.lower()
        data = data.split()
        return SearchIndex._ngram_list(data)

    def add_to_index(self, doc_content):
        """

        :param doc_content:
        :return:
        """

        # generate an new id
        doc_md5 = md5()
        doc_md5.update(doc_content.encode())
        doc_id = doc_md5.digest()

        if doc_id in self.DOCS_LENGTHS:
            return
        self._add_to_index(doc_id, self.gramify(doc_content))
        return doc_id

    def _add_to_index(self, doc, doc_ngrams):

        for i, gram in enumerate(doc_ngrams):
            key = tuple([gram, doc])
            if key not in self.INDEX:
                self.INDEX[key] = list()
            self.INDEX[key].append(i)

            if gram not in self.NGRAMS_2_DOCS:
                self.NGRAMS_2_DOCS[gram] = dict()
            self.NGRAMS_2_DOCS[gram][doc] = 1  # Value does not really matter
        self.NUMBER_DOCS += 1
        self.DOCS_LENGTHS[doc] = len(doc_ngrams)

    # def search_score_naive(term):
    #     """
    #     Score basiert lediglich auf der Anzahl der Vorkommen der n-grams im Suchindex.
    #     """
    #     term_index = _add_to_index(term)
    #     matches = 0
    #     term_grams = [term[i:i+CHARS_IN_GRAM] for i in range(0, len(term) - CHARS_IN_GRAM + 1)]
    #     for gram in term_grams:
    #         if gram in INDEX:
    #             position = INDEX[gram]
    #             matches += 1
    #     return matches / len(term_grams)

    def search(self, term):
        # Avoid division by zero
        if len(self.NGRAMS_2_DOCS) == 0:
            return Score()

        if len(term) == 0:
            # Avoid division by zero in _compute_score
            return Score()

        grams = self.gramify(term)
        return self._search(grams)

    def _search(self, term_ngrams):
        """
        Score basiert auf Abständen der n-grams zum ersten n-gram, der ein Treffer ist.
        Param: term_ngrams - list of n-grams
        """
        score = Score()
        position_gram0 = dict()

        for position, gram in enumerate(term_ngrams):
            position_gram0, score_gram = self._compute_score(position_gram0, position, gram, len(term_ngrams))

            score.update(score_gram)
        return score

    def _compute_score(self, position_gram0, position_gram, gram, term_length):
        if gram not in self.NGRAMS_2_DOCS:
            return position_gram0, Score()

        docs = self.NGRAMS_2_DOCS[gram]

        min_dist = float("inf")
        score_gram = Score()
        for key in [tuple([gram, doc]) for doc in docs.keys()]:
            entries_for_doc = self.INDEX[key]
            doc = key[1]

            if doc not in position_gram0:
                position_gram0[doc] = entries_for_doc[0]

            for position_doc in entries_for_doc:
                dist = abs(position_doc - position_gram0[doc] - position_gram)
                if dist < min_dist:
                    min_dist = dist

            score = (1 - min_dist / self.DOCS_LENGTHS[doc]) / term_length
            #print("SCORE {} in {} = {}".format(gram, doc, score))

            score_gram.update(Score({
                doc: score
            }))

        return position_gram0, score_gram

    def __sizeof__(self):
        size = 0
        for key in self.INDEX.keys():
            size += sys.getsizeof(key)
            size += sys.getsizeof(1) * len(self.INDEX[key])
        for key in self.NGRAMS_2_DOCS.keys():
            size += sys.getsizeof(key)
            size += sum([sys.getsizeof(el) for el in self.NGRAMS_2_DOCS[key].keys()])

        for key in self.DOCS_LENGTHS.keys():
            size += sys.getsizeof(key)
            size += sys.getsizeof(1)

        return size