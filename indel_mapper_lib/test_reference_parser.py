import unittest
from .reference_parser import ReferenceParser
from .read import Read


class TestReferenceParser(unittest.TestCase):

    def test_reads(self):
        reference_to_reads = {"foo": [Read(query_name='lion',
                                           reference_positions=[1,2],
                                           query_sequence="cat",
                                           aligned_pairs=()),
                                      Read(query_name='wolf',
                                           reference_positions=[4,5],
                                           query_sequence="tag",
                                           aligned_pairs=())]}

        fake_csv_file = [('foo','cat','ccaattgg','ngg'),
                         ('bar','tag','ggaattttg','ngg')]
        references = ReferenceParser(fake_csv_file, reference_to_reads).references()

        self.assertEqual(len(references), 2)

        foo_reference = references[0]
        bar_reference = references[1]

        self.assertEqual(len(foo_reference.reads), 2)
        self.assertEqual(foo_reference.reads[0].query_name,
                         reference_to_reads["foo"][0].query_name)
        self.assertEqual(foo_reference.reads[1].query_name,
                         reference_to_reads["foo"][1].query_name)

        self.assertEqual(len(bar_reference.reads), 0)
        self.assertEqual(foo_reference.name, 'foo')
        self.assertEqual(foo_reference.n20, 'CAT')
        self.assertEqual(foo_reference.sequence, 'CCAATTGG')
        self.assertEqual(foo_reference.pam, 'NGG')
