import unittest

from .sequence_diff import SequenceDiff
from .diff_components import DiffDeletion
from .diff_components import DiffInsertion
from .diff_components import DiffMatch
from .diff_components import DiffMutation


class TestSequenceDiff(unittest.TestCase):
    def test_validation(self):
        with self.assertRaises(ValueError):
            SequenceDiff("AT", "TAT")
        with self.assertRaises(ValueError):
            SequenceDiff("A||TA", "AT||A")

    def test_tokenizer(self):
        diff = SequenceDiff("GATT___ACA||AGGT__C",
                            "GAT_GGCA__||AGC_AGC")
        expected_changes = [DiffMatch("GAT", "GAT"),
                            DiffDeletion("T", "_"),
                            DiffInsertion("___", "GGC"),
                            DiffMatch("A", "A"),
                            DiffDeletion("CA", "__"),
                            DiffMatch("AG", "AG"),
                            DiffMutation("G", "C"),
                            DiffDeletion("T", "_"),
                            DiffInsertion("__", "AG"),
                            DiffMatch("C", "C")]
        self.assertEqual(diff.changes, expected_changes)

    def test_description(self):
        diff = SequenceDiff("GATT___ACA||AGGT__C",
                            "GAT_GGCA__||AGC_AGC")
        self.assertEqual(diff.description(),
                         "1 deletion (T), 3 insertions (GGC), 1 match, "
                         "2 deletions (CA), 2 matches, 1 mutation (G to C), "
                         "1 deletion (T), 2 insertions (AG)")

    def test_description_without_cutsite(self):
        diff = SequenceDiff("GATT___ACAAGGT__C",
                            "GAT_GGCA__AGC_AGC")
        self.assertEqual(diff.description(),
                         "1 deletion (T), 3 insertions (GGC), 1 match, "
                         "2 deletions (CA), 2 matches, 1 mutation (G to C), "
                         "1 deletion (T), 2 insertions (AG)")
