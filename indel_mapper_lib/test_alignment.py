import unittest
from .alignment import Alignment

class TestAlignment(unittest.TestCase):
    def test_equality(self):
        self.assertEqual(Alignment("foo", "bar"),
                         Alignment("foo", "bar"))
        self.assertNotEqual(Alignment("foo", "bar"),
                            Alignment("bar", "foo"))

    def test_repr(self):
        self.assertEqual(str(Alignment("foo", "bar")),
                         "(foo, bar)")

    def test_has_unmatched_bases_at_index(self):
        test_alignment = Alignment("catca_", "_atcat")

        self.assertTrue(test_alignment.has_unmatched_bases_at(0))
        self.assertFalse(test_alignment.has_unmatched_bases_at(1))
        self.assertTrue(test_alignment.has_unmatched_bases_at(-1))

    def test_starts_with(self):

        container_alignment = Alignment("gammadelta", "alphabeta")
        alignment_a = Alignment("gamma", "alpha")
        alignment_b = Alignment("omega", "beta")

        self.assertTrue(container_alignment.starts_with(alignment_a))
        self.assertFalse(container_alignment.starts_with(alignment_b))

    def test_to_dict(self):
        self.assertEqual(Alignment("foo", "bar").to_dict(),
                         {
                             "reference": "foo",
                             "read": "bar"
                         }
        )
