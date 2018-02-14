class SearchIndex():
    # Class variables; set by create_index()
    SEARCH_INDEX = dict()
    SEARCH_INDEX_LENGTH = 0

    CHARS_IN_GRAM = 3

    @staticmethod
    def extract_alphanum_data(data):
        result = ""
        punctuation = ".,:-'\"?!<>()[]&"
        for letter in data:
            if letter not in punctuation:
                result += letter
        return result

    def create_index(self, data):

        alphanum_data = self.extract_alphanum_data(data)
        words = alphanum_data.split()
        start_i = 0
        for word in words:
            for i in range(start_i, len(word) - self.CHARS_IN_GRAM + 1):
                gram = word[i:i + self.CHARS_IN_GRAM]
                if not gram in self.SEARCH_INDEX:
                    self.SEARCH_INDEX[gram] = list()
                self.SEARCH_INDEX[gram].append(i)
            start_i = i
            self.SEARCH_INDEX_LENGTH += i

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

    @classmethod
    def create_gram_list(cls, data):
        result = list()

        for i in range(0, len(data) - cls.CHARS_IN_GRAM + 1):
            result.append(data[i:i + cls.CHARS_IN_GRAM])
        return result

    def search_score(self, term):
        """
        Score basiert auf Abständen der n-grams zum ersten n-gram, der ein Treffer ist.
        """
        score = 0
        position_first_match = None
        term_grams = self.create_gram_list(term)
        if len(term_grams) == 0:
            # Avoid division by zero
            return 0.0
        for position_in_term, gram in enumerate(term_grams):
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
            if min_dist == 0: min_dist = 1

            score_gram = 1 - min_dist / self.SEARCH_INDEX_LENGTH
            print("{}, Position {}, rel. distance {}, score gram {}".format(gram, position, min_dist, score_gram))
            score += score_gram
        return score / len(term_grams)
