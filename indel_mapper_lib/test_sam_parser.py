import unittest
from unittest.mock import patch
from .sam_parser import SamParser


class TestSamParser(unittest.TestCase):

    def mock_fetch(self):
        class FakeAlignedSegment(object):
            def __init__(self, query_name=None,
                         reference_name=None,
                         reference_positions=None,
                         cigartuples=(),
                         query_sequence=None,
                         aligned_pairs=()):
                self.query_name = query_name
                self.cigartuples = cigartuples
                self.query_sequence = query_sequence
                self.aligned_pairs = aligned_pairs
                if reference_name:
                    self.reference_name = reference_name
                if reference_positions:
                    self.reference_positions = reference_positions

            def get_reference_positions(self, full_length):
                return self.reference_positions

            def get_aligned_pairs(self):
                return self.aligned_pairs

        segment_a = FakeAlignedSegment(query_name='foo')
        segment_b = FakeAlignedSegment(query_name='bar',
                                       reference_name='cats',
                                       query_sequence='cattttt',
                                       reference_positions=())
        segment_c = FakeAlignedSegment(query_name='baz',
                                       reference_name='dogs',
                                       query_sequence='taggggg',
                                       reference_positions=(1, 2, None,
                                                            None, 3),
                                       cigartuples=((0, 1), (0, 2), (2, None),
                                                    (2, None), (0, 3)))

        return [segment_a, segment_b, segment_c]

    @patch('indel_mapper_lib.sam_parser.SamParser._fetch')
    def test_create_reads_from_sam(self, mock_fetcher):
        sam_file = "fake alignment file"
        mock_values = self.mock_fetch()
        mock_fetcher.return_value = mock_values

        reference_name_to_reads = SamParser(sam_file).reference_name_to_reads_dict()
        expected_reference_name = mock_values[-1].reference_name

        self.assertEqual(len(reference_name_to_reads), 1)
        self.assertTrue(expected_reference_name in reference_name_to_reads)
        self.assertEqual(len(reference_name_to_reads[expected_reference_name]), 1)
        self.assertEqual(reference_name_to_reads[expected_reference_name][0].query_name,
                         mock_values[-1].query_name)
