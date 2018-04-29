class Score:
    def __init__(self, initial_score=None):
        if not initial_score:
            self.score = dict()
            return
        if not isinstance(initial_score, dict):
            raise ValueError("Not a dict.")
        else:
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

    def value(self):
        # Convert keys from b'' to a hex representation
        return {"".join(["{:02x}".format(x) for x in k]):v \
                for k,v in self.score.items()}

    def equals(self, other):
        if not isinstance(other, Score):
            return False
        return self.value() == other.value()

