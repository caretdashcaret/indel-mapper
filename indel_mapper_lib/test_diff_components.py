import unittest

from .diff_components import DiffDeletion
from .diff_components import DiffInsertion
from .diff_components import DiffMatch
from .diff_components import DiffMutation


class TestDiffDeletion(unittest.TestCase):
    def test_is_match(self):
        self.assertFalse(DiffDeletion("ACT", "___").is_match())

    def test_repr(self):
        self.assertEqual(str(DiffDeletion("A", "_")),
                         "1 deletion (A)")
        self.assertEqual(str(DiffDeletion("ACT", "___")),
                         "3 deletions (ACT)")


class TestDiffInsertion(unittest.TestCase):
    def test_is_match(self):
        self.assertFalse(DiffInsertion("___", "ACT").is_match())

    def test_repr(self):
        self.assertEqual(str(DiffInsertion("_", "A")),
                         "1 insertion (A)")
        self.assertEqual(str(DiffInsertion("___", "ACT")),
                         "3 insertions (ACT)")


class TestDiffMatch(unittest.TestCase):
    def test_is_match(self):
        self.assertTrue(DiffMatch("ACT", "ACT").is_match())

    def test_repr(self):
        self.assertEqual(str(DiffMatch("A", "A")), "1 match")
        self.assertEqual(str(DiffMatch("ACT", "ACT")), "3 matches")


class TestDiffMutation(unittest.TestCase):
    def test_is_match(self):
        self.assertFalse(DiffMutation("ACT", "GTA").is_match())

    def test_repr(self):
        self.assertEqual(str(DiffMutation("A", "G")), "1 mutation (A to G)")
        self.assertEqual(str(DiffMutation("ACT", "GTA")), "3 mutations (ACT to GTA)")
