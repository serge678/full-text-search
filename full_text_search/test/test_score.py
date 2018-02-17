from unittest import TestCase, main
from ..score import Score


class TestScore(TestCase):
    def test_init_empty(self):
        score = Score()
        self.assertDictEqual(dict(), score.value())

    def test_update(self):
        score = Score({
            0: 0.01,
            1: 0.9,
        })
        score_gram = Score({
            1: 0.01,
            2: 0.01,
        })
        score_exp = Score({
            0: 0.01,
            1: 0.91,
            2: 0.01,
        })
        score.update(score_gram)
        self.assertTrue(score_exp.equals(score))


if __name__ == '__main__':
    main()
