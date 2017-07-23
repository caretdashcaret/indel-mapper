import unittest
from .read import Read


class TestRead(unittest.TestCase):

    def test_create_read(self):

        query_name = "foo"
        reference_positions = [1, 2, 3, 4, None, None, 5]
        query_sequence = "gatcatcattta"
        aligned_pairs = ((1, 1), (2, 2),
                         (3, 3), (4, 4),
                         (5, None), (6, None),
                         (7, 5))

        test_read = Read(query_name,
                         reference_positions,
                         query_sequence,
                         aligned_pairs)

        self.assertEqual(test_read.query_name, query_name)
        self.assertEqual(test_read.query_sequence, query_sequence.upper())
        self.assertEqual(test_read.aligned_pairs, aligned_pairs)

    def test_create_indels_for_read(self):
        reference_positions_a = [1, 2, 3, 4,
                                 None, None, None, 5,
                                 6, 7, None, None,
                                 None, None, 8]
        read_a = Read(query_name="",
                      reference_positions=reference_positions_a,
                      query_sequence="",
                      aligned_pairs=())
        indels_a = read_a.indels

        reference_positions_b = [3, 4, 5, 10, 11, 12, None, None, 13]
        read_b = Read(query_name="",
                      reference_positions=reference_positions_b,
                      query_sequence="",
                      aligned_pairs=())
        indels_b = read_b.indels

        self.assertEqual(len(indels_a), 2)

        self.assertEqual(indels_a[0].start_index, 4)
        self.assertEqual(indels_a[0].end_index, 5)
        self.assertEqual(indels_a[0].length, 3)
        self.assertFalse(indels_a[0].is_deletion)
        self.assertTrue(indels_a[0].is_insertion)

        self.assertEqual(indels_a[1].start_index, 7)
        self.assertEqual(indels_a[1].end_index, 8)
        self.assertEqual(indels_a[1].length, 4)
        self.assertFalse(indels_a[1].is_deletion)
        self.assertTrue(indels_a[1].is_insertion)

        self.assertEqual(len(indels_b), 2)

        self.assertEqual(indels_b[0].start_index, 5)
        self.assertEqual(indels_b[0].end_index, 10)
        self.assertEqual(indels_b[0].length, 4)
        self.assertTrue(indels_b[0].is_deletion)
        self.assertFalse(indels_b[0].is_insertion)

        self.assertEqual(indels_b[1].start_index, 12)
        self.assertEqual(indels_b[1].end_index, 13)
        self.assertEqual(indels_b[1].length, 2)
        self.assertFalse(indels_b[1].is_deletion)
        self.assertTrue(indels_b[1].is_insertion)

    def test_valid_indels(self):
        reference_positions_a = [None, None, None, 0, 1, 2]
        read_a = Read(query_name="",
                      reference_positions=reference_positions_a,
                      query_sequence="",
                      aligned_pairs=())
        indels_a = read_a.valid_indels

        self.assertEqual(len(indels_a), 0)
