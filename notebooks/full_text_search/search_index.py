class SearchIndex():

    CHARS_IN_GRAM = 3

    def __init__(self):
        self.SEARCH_INDEX        = dict()
        self.SEARCH_INDEX_LENGTH = 0

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

        :param data: list of words
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

    def create_index(self, data_ngrams):
        """

        :param data_ngrams: Expects list of gram for the document/term.
                            Use gramify() for that purpose.
        :return:
        """

        for i, gram in enumerate(data_ngrams):
            if gram not in self.SEARCH_INDEX:
                self.SEARCH_INDEX[gram] = list()
            self.SEARCH_INDEX[gram].append(i)
        self.SEARCH_INDEX_LENGTH = i

    # def search_score_naive(term):
    #     """
    #     Score basiert lediglich auf der Anzahl der Vorkommen der n-grams im Suchindex.
    #     """
    #     term_index = create_index(term)
    #     matches = 0
    #     term_grams = [term[i:i+CHARS_IN_GRAM] for i in range(0, len(term) - CHARS_IN_GRAM + 1)]
    #     for gram in term_grams:
    #         if gram in SEARCH_INDEX:
    #             position = SEARCH_INDEX[gram]
    #             matches += 1
    #     return matches / len(term_grams)

    def search_score(self, term_ngrams):
        """
        Score basiert auf Abständen der n-grams zum ersten n-gram, der ein Treffer ist.
        Param: term_ngrams - list of n-grams
        """
        score = 0
        position_first_match = None

        if len(term_ngrams) == 0:
            # Avoid division by zero
            return 0.0
        for position_in_term, gram in enumerate(term_ngrams):
            # Initialise: not in index
            positions = [float("inf")]
            if gram not in self.SEARCH_INDEX:
                continue

            positions = self.SEARCH_INDEX[gram]

            if not position_first_match:
                # TODO: this is a simplification. Takes always first match
                position_first_match = positions[0]

            # Determine best match and it's distance
            min_dist = float("inf")
            for position in positions:
                dist = abs(position - position_first_match - position_in_term)
                if dist < min_dist: min_dist = dist

            # Avoid division by zero
            if self.SEARCH_INDEX_LENGTH == 0:
                return 0.0

            score_gram = 1 - min_dist / self.SEARCH_INDEX_LENGTH
            print("{}, Position {}, rel. distance {}, score gram {}".format(gram, position, min_dist, score_gram))
            score += score_gram
        return score / len(term_ngrams)
