import unittest
from .reference import Reference
from .indel import Indel
from .read import Read


class TestReference(unittest.TestCase):

    def test_create_reference(self):
        name = "foo"
        n20 = "aaaaggg"
        sequence = "catcatcatcat"
        pam = "ngg"
        reads = [1]

        reference = Reference(name, n20, sequence, pam, reads)

        self.assertEqual(reference.name, name)
        self.assertEqual(reference.n20, n20.upper())
        self.assertEqual(reference.sequence, sequence.upper())
        self.assertEqual(reference.pam, pam.upper())
        self.assertEqual(reference.reverse_complement_n20, "CCCTTTT")

    def test_is_ngg_pam(self):
        ngg_reference = Reference("", "", "", "ngg", [])
        ccn_reference = Reference("", "", "", "ccn", [])

        self.assertTrue(ngg_reference.is_ngg())
        self.assertFalse(ccn_reference.is_ngg())

    def test_is_valid(self):
        ngg_reference = Reference("", "cat", "ccattgg", "ngg", [])
        bad_ngg_reference = Reference("", "cat", "ccatt", "ngg", [])
        ccn_reference = Reference("", "cat", "ccgcatt", "ccg", [])
        bad_ccn_reference = Reference("", "cat", "ttccatt", "ccg", [])
        rc_ngg_reference = Reference("", "atg", "ccattgg", "ngg", [])
        rc_ccn_reference = Reference("", "atg", "ccgcatt", "cgg", [])

        self.assertTrue(ngg_reference.is_valid)
        self.assertFalse(bad_ngg_reference.is_valid)
        self.assertTrue(ccn_reference.is_valid)
        self.assertFalse(bad_ccn_reference.is_valid)
        self.assertTrue(rc_ngg_reference.is_valid)
        self.assertTrue(rc_ccn_reference.is_valid)

    def test_cutsite(self):
        n20 = "aaaatttc"
        sequence = "tactactacaaaatttcnggt"
        pam = "ngg"

        ngg_reference = Reference("", n20, sequence, pam, [])

        n20 = "cattttg"
        sequence = "ccgcattttgaaa"
        pam = "ccn"

        ccn_reference = Reference("", n20, sequence, pam, [])

        self.assertEqual(ngg_reference.n20_pam_index(), 16)
        self.assertEqual(ngg_reference.cutsite_index(), 13)
        self.assertEqual(ccn_reference.n20_pam_index(), 3)
        self.assertEqual(ccn_reference.cutsite_index(), 6)

        n20 = "GCCATTTACACTTCTTTTG"
        sequence = "AAGGGGGTTTGTTCTCTGGTGGGCAGGAGTGGGGGGTCGC" \
                   "AAGGGCTCAGTGGGGGTGCTTTTTGAGCCAGGATGAGCCA" \
                   "GGAAAAGGACTTTCACAAGGTAATGTCATCACTTAAGGGA" \
                   "AGGACCGGCCATTTACACTTCTTTTGTGGTGGAATGTCAT" \
                   "CAGTTAAGGCGGGGCAGGGCATTTTCACTTCTTTTGTGAT" \
                   "TCTTCAGTTACTTCAGGCCATCTGGG"
        pam = "NGG"

        long_reference = Reference("", n20, sequence, pam, [])

        self.assertEqual(long_reference.n20_pam_index(), 145)
        self.assertEqual(long_reference.cutsite_index(), 142)

    def test_pam_and_n20_index(self):
        n20 = "GCCATTTACACTTCTTTTG"
        sequence = "AAGGGGGTTTGTTCTCTGGTGGGCAGGAGTGGGGGGTCGC" \
                   "AAGGGCTCAGTGGGGGTGCTTTTTGAGCCAGGATGAGCCA" \
                   "GGAAAAGGACTTTCACAAGGTAATGTCATCACTTAAGGGA" \
                   "AGGACCGGCCATTTACACTTCTTTTGTGGTGGAATGTCAT" \
                   "CAGTTAAGGCGGGGCAGGGCATTTTCACTTCTTTTGTGAT" \
                   "TCTTCAGTTACTTCAGGCCATCTGGG"
        pam = "NGG"

        long_reference = Reference("", n20, sequence, pam, [])

        self.assertEqual(long_reference.pam_index(), 148)
        self.assertEqual(long_reference.n20_index(), 126)

    def test_distance_to_cutsite(self):
        n20 = "aaaatttc"
        sequence = "tactactacaaaatttcnggt"
        pam = "ngg"

        # cutsite is at 13
        ngg_reference = Reference("", n20, sequence, pam, [])

        indel_a = Indel(start_index=11,
                        end_index=12,
                        length=4,
                        is_deletion=False)
        indel_b = Indel(start_index=10,
                        end_index=15,
                        length=6,
                        is_deletion=True)
        indel_c = Indel(start_index=13,
                        end_index=14,
                        length=4,
                        is_deletion=False)
        indel_d = Indel(start_index=18,
                        end_index=20,
                        length=2,
                        is_deletion=True)

        self.assertEqual(ngg_reference.distance_to_cutsite(indel_a), -1)
        self.assertEqual(ngg_reference.distance_to_cutsite(indel_b), 0)
        self.assertEqual(ngg_reference.distance_to_cutsite(indel_c), 0)
        self.assertEqual(ngg_reference.distance_to_cutsite(indel_d), 5)

    def test_additional_cutsite(self):
        n20 = "ccccggggaaaa"
        sequence = "aaacctccccggggaaaattt"
        pam = "ccn"

        ccn_reference = Reference("", n20, sequence, pam, [])

        self.assertEqual(ccn_reference.n20_pam_index(), 6)
        self.assertEqual(ccn_reference.cutsite_index(), 9)


    def test_reads_with_indels_near_the_cutsite(self):
        n20 = "aaaatttc"
        sequence = "tactactacaaaatttcnggt"
        pam = "ngg"

        reference_positions_a = [8, None, None, None,
                                 9, 10, 11, None,
                                 None, None, None, 12,
                                 13, 14]
        read_a = Read("a", reference_positions_a, "", ())

        reference_positions_b = [10, 15]
        read_b = Read("b", reference_positions_b, "", ())

        reference_positions_c = [10, 11, 12, 13, 14]
        read_c = Read("c", reference_positions_c, "", ())

        reference_positions_d = [13, None, None, None, None, 14]
        read_d = Read("d", reference_positions_d, "", ())

        reference_positions_e = [18, 20]
        read_e = Read("e", reference_positions_e, "", ())

        reference_positions_f = [None, None, None, 0, 1, 2]
        read_f = Read("f", reference_positions_f, "", ())

        reads = [read_a, read_b, read_c, read_d, read_e, read_f]

        ngg_reference = Reference("", n20, sequence, pam, reads, max_dist_to_cutsite=1)

        reads_with_indels_near_the_cutsite = ngg_reference.reads_with_indels_near_the_cutsite

        self.assertEqual(len(reads_with_indels_near_the_cutsite), 3)
        self.assertEqual([read.query_name for read in reads_with_indels_near_the_cutsite],
                         ["a", "b", "d"])

        ngg_reference = Reference("", n20, sequence, pam, [read_e], max_dist_to_cutsite=1)
        reads_with_indels_near_the_cutsite = ngg_reference.reads_with_indels_near_the_cutsite

        self.assertEqual(len(reads_with_indels_near_the_cutsite), 0)
        self.assertFalse(ngg_reference.has_reads_with_indels_near_the_cutsite())

        ngg_reference = Reference("", n20, sequence, pam, [read_e], max_dist_to_cutsite=5)
        reads_with_indels_near_the_cutsite = ngg_reference.reads_with_indels_near_the_cutsite

        self.assertEqual(len(reads_with_indels_near_the_cutsite), 1)
        self.assertTrue(ngg_reference.has_reads_with_indels_near_the_cutsite())
