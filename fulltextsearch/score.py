class Score:
    """
    A dictionary of document ids with their scores.
    """
    def __init__(self, initial_score=None):
        if not initial_score:
            self.score = dict()
            return
        if not isinstance(initial_score, dict):
            raise ValueError("Not a dict.")

        for k in initial_score.keys():
            if not isinstance(k, bytes):
                raise ValueError("Not of type bytes: '%s'" % k)

        self.score = initial_score

    def update(self, score_gram):
        """
        Updates total score with the score of ngram
        :param score_gram:
        :return:
        """

        for doc, score_in_doc in score_gram.score.items():
            if doc not in self.score:
                self.score[doc] = score_in_doc
            else:
                self.score[doc] += score_in_doc

    @staticmethod
    def hex_repr(k):
        """
        Converts id to a human readable hex representation
        :param k: id as a b'' string
        :return:
        """
        return "".join(["{:02x}".format(x) for x in k])

    def value(self):
        """
        Returns the list of relevant document ids

        :return: List of tuples: doc_ids with their relevance score
        """
        res = {self.hex_repr(k): v for k, v in self.score.items()}
        # Sort by value
        return sorted(res.items(), key=lambda x:x[1], reverse=True)

    def equals(self, other):
        if not isinstance(other, Score):
            return False
        return self.value() == other.value()
