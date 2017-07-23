import unittest
from .read_reference_relationship import ReadReferenceRelationship

class TestReadReferenceRelationship(unittest.TestCase):

    def create_relationship(self, aligned_pair_index, is_ngg=True):

        aligned_pairs = [(0, 14), (1, 15), (2, 16), (3, None), (4, None), (5, None), (6, 17), (7, 18), (8, 19), (9, 20), (10, 21), (11, 22), (12, 23), (13, 24), (14, 25), (15, 26), (16, 27), (17, 28), (18, 29), (19, 30), (20, 31), (21, 32), (22, 33), (23, 34), (24, 35), (25, 36), (26, 37), (27, 38), (28, 39), (29, 40), (30, 41), (31, 42), (32, 43), (33, 44), (34, 45), (35, 46), (36, 47), (37, 48), (38, 49), (39, 50), (40, 51), (41, 52), (42, 53), (43, 54), (44, 55), (45, 56), (46, 57), (47, 58), (48, 59), (49, 60), (50, 61), (51, 62), (52, 63), (53, 64), (54, 65), (55, 66), (56, 67), (57, 68), (58, 69), (59, 70), (60, 71), (61, 72), (62, 73), (63, 74), (64, 75), (65, 76), (66, 77), (67, 78), (68, 79), (69, 80), (70, 81), (71, 82), (72, 83), (73, 84), (74, 85), (75, 86), (76, 87), (77, 88), (78, 89), (79, 90), (80, 91), (81, 92), (82, 93), (83, 94), (84, 95), (85, 96), (86, 97), (87, 98), (88, 99), (89, 100), (90, 101), (91, 102), (92, 103), (93, 104), (94, 105), (95, 106), (96, 107), (97, 108), (98, 109), (99, 110), (100, 111), (101, 112), (102, 113), (103, 114), (104, 115), (105, 116), (None, 117), (106, 118), (107, 119), (108, 120), (109, 121), (110, 122), (111, 123), (112, 124), (113, 125), (114, 126), (115, 127), (116, 128), (117, 129), (118, 130), (119, 131)]
        reference_sequence = "AGGAACTGGGAGAGGACGATCCGGTTAGGGAGGTTGGGGA" \
                             "ACTAATCTCAACGCTGCGTTTACAGATGAAGCCGCTTTTA" \
                             "TATGGCGTATATGTTTGCTTAGAGGGGCCGACGGAGATTA" \
                             "GGAGAAGCCATCCTTTGGCGCCAATGATCAAAGCGTCTGC" \
                             "CAAGGAGAAGAAGCCAAGGGATGGGCCTTTCAGAGAGGGC" \
                             "AAGGAGTCATGCTGCTCTGGATGCCAGTGTCAGGACAAG"
        read_sequence = "TCCGCAGATCCGGTTAGGGAGGTTGGGGAACTAATCTCAA" \
                        "CGCTGCGTTTACAGATGAAGCCGCTTTTATATGGCGTATA" \
                        "TGTTTGCTTAGAGGGGCCGACGGAGATAGGAGAAGCCATC" \
                        "CTTTGGCGCCAATGATCAAAGCGTCTGCCAAGGAGAAGAA" \
                        "GCCAAGGGATGGGCCTTTCAGAGAGGGCAAGGAGTCATGC" \
                        "TGCTCTGGATGCCAGTGTCAGGACAA"
        pam_index = 121
        n20_index = 98

        return ReadReferenceRelationship(aligned_pair_index,
                                         aligned_pairs,
                                         reference_sequence,
                                         read_sequence,
                                         pam_index,
                                         n20_index,
                                         is_ngg)

    def test_is_insertion(self):
        relationship = self.create_relationship(aligned_pair_index=4)
        self.assertTrue(relationship.is_insertion())

        relationship = self.create_relationship(aligned_pair_index=2)
        self.assertFalse(relationship.is_insertion())

        relationship = self.create_relationship(aligned_pair_index=106)
        self.assertFalse(relationship.is_insertion())

    def test_is_deletion(self):
        relationship = self.create_relationship(aligned_pair_index=20)
        self.assertFalse(relationship.is_deletion())

        relationship = self.create_relationship(aligned_pair_index=2)
        self.assertFalse(relationship.is_deletion())

        relationship = self.create_relationship(aligned_pair_index=106)
        self.assertTrue(relationship.is_deletion())

    def test_is_mismatch(self):
        relationship = self.create_relationship(aligned_pair_index=20)
        self.assertFalse(relationship.is_mismatch())

        relationship = self.create_relationship(aligned_pair_index=3)
        self.assertTrue(relationship.is_mismatch())

        relationship = self.create_relationship(aligned_pair_index=106)
        self.assertTrue(relationship.is_mismatch())

        relationship = self.create_relationship(aligned_pair_index=0)
        self.assertTrue(relationship.is_mismatch())

        relationship = self.create_relationship(aligned_pair_index=1)
        self.assertTrue(relationship.is_mismatch())

    def test_is_between_pam_and_n20_for_ccn(self):

        relationship = self.create_relationship(aligned_pair_index=100, is_ngg=False)
        self.assertTrue(relationship.is_between_pam_and_n20())

        relationship = self.create_relationship(aligned_pair_index=86, is_ngg=False)
        self.assertFalse(relationship.is_between_pam_and_n20())

        relationship = self.create_relationship(aligned_pair_index=110, is_ngg=False)
        self.assertFalse(relationship.is_between_pam_and_n20())

    def test_is_between_pam_and_n20_for_ngg(self):

        relationship = self.create_relationship(aligned_pair_index=100)
        self.assertTrue(relationship.is_between_pam_and_n20())

        relationship = self.create_relationship(aligned_pair_index=86)
        self.assertFalse(relationship.is_between_pam_and_n20())

        relationship = self.create_relationship(aligned_pair_index=110)
        self.assertTrue(relationship.is_between_pam_and_n20())

        relationship = self.create_relationship(aligned_pair_index=111)
        self.assertFalse(relationship.is_between_pam_and_n20())

    def test_next_to_mismatch_or_indel(self):
        relationship = self.create_relationship(aligned_pair_index=100)
        self.assertFalse(relationship.next_to_mismatch_or_indel())

        relationship = self.create_relationship(aligned_pair_index=105)
        self.assertTrue(relationship.next_to_mismatch_or_indel())

        relationship = self.create_relationship(aligned_pair_index=106)
        self.assertFalse(relationship.next_to_mismatch_or_indel())

        relationship = self.create_relationship(aligned_pair_index=107)
        self.assertTrue(relationship.next_to_mismatch_or_indel())

        relationship = self.create_relationship(aligned_pair_index=5)
        self.assertTrue(relationship.next_to_mismatch_or_indel())
