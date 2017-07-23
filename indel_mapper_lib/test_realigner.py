import unittest
from .realigner import Realigner
from .alignment import Alignment

class TestRealigner(unittest.TestCase):
    def assert_realignment(self, input_pair, output_pair):
        self.assertEqual(
            Realigner(Alignment(*input_pair)).align(),
            Alignment(*output_pair))

    def test_shift_deletions_closer(self):
        self.assert_realignment(
            ["ACCACT||",
             "A___C_||"],
            ["ACCACT||",
             "AC____||"])
        self.assert_realignment(
            ["A||TTT",
             "A||T_T"],
            ["A||TTT",
             "A||_TT"])

    def test_shift_insertions_away(self):
        self.assert_realignment(
            ["G_TT||",
             "GTTT||"],
            ["GTT_||",
             "GTTT||"])

    def test_shift_clusters(self):
        self.assert_realignment(
            ["CATCAT||",
             "___CAT||"],
            ["CATCAT||",
             "CAT___||"])

    def test_reading_on_the_boundary(self):
        self.assert_realignment(
            ["AGC|CAGAA||TGG|GGG|",
             "A__|_____||_GG|GGG|"],
            ["AGC|CAGAA||TGG|GGG|",
             "A__|_____||_GG|GGG|"])
