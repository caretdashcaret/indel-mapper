import unittest
from .sequence import Sequence


class TestSequence(unittest.TestCase):
    def test_creating_valid_sequences(self):
        invalid_sequence = "GANNACA"
        with self.assertRaises(ValueError):
            Sequence(invalid_sequence)

    def test_str(self):
        seq = "GATTACA"
        self.assertEqual(str(Sequence(seq)), seq)

    def test_object_equality(self):
        self.assertEqual(Sequence("A"), Sequence("A"))
        self.assertNotEqual(Sequence("A"), Sequence("T"))

    def test_reverse_complement(self):
        self.assertEqual(Sequence("GATTACA").reverse_complement(),
                         Sequence("TGTAATC"))
