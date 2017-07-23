import unittest
from .reference import Reference
from .reference_presenter import ReferencePresenter

class TestReferencePresenter(unittest.TestCase):

    def test_reference_presenter(self):
        ref = ReferencePresenter(Reference("foo", "", "", "", []), [])
        self.assertEqual(ref.csv_row_prefix_cells(), ["foo", 0])

    def test_to_dict(self):
        ref = ReferencePresenter(Reference("foo", "aaa", "aaaag", "ngg", []), [])
        self.assertEqual(ref.to_dict(),
                         {
                             "name": "foo",
                             "sequence": "AAAAG",
                             "n20": "AAA",
                             "pam": "NGG",
                             "has_mutation_clusters": False,
                             "total_reads": 0,
                             "mutation_clusters": []
                         }
        )
