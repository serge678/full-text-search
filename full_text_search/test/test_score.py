from unittest import TestCase, main
from ..score import Score


class TestScore(TestCase):
    def test_hex_repr(self):
        score = Score()
        self.assertEqual(score.hex_repr(b'0'), '30')

    def test_init_empty(self):
        score = Score()
        self.assertDictEqual(dict(), score.value())

    def test_update(self):
        score = Score({
            b'0': 0.01,
            b'1': 0.9,
        })
        score_gram = Score({
            b'1': 0.01,
            b'2': 0.01,
        })
        score_exp = Score({
            b'0': 0.01,
            b'1': 0.91,
            b'2': 0.01,
        })
        score.update(score_gram)
        self.assertTrue(score_exp.equals(score))


if __name__ == '__main__':
    main()
