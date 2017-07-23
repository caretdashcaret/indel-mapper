import unittest
from .cas9_indicator_inserter import Cas9IndicatorInserter
from .read import Read
from .reference import Reference
from .presenter import Presenter

class TestCas9IndicatorInserter(unittest.TestCase):

    def test_insert_indicators_in_ccn_array(self):
        reference_sequence = "ATTA__G---------------------------------" \
                             "----------------------------------------" \
                             "----------------------------------------" \
                             "-----------------------CCTAAGGAAGTTTCAGC" \
                             "AAGGC-CTA------TCT_G---CCA----CAGT-----G" \
                             "AG--GTC---T_________GACTCCC"
        reference = list(reference_sequence)

        read_sequence = "GTTCGCG---------------------------------" \
                        "----------------------------------------" \
                        "----------------------------------------" \
                        "-----------------------CCTAAGG_AGTTTCCAG" \
                        "AAGGC-CCA------TTTGG---CAA----CGTT-----G" \
                        "GG--GCC---TGCCCCCCGGGATTGGG"
        read = list(read_sequence)

        cutsite_index = 179
        pam_index = 173
        n20_pam_index = 176
        n20_index = 195
        aligned_pairs = [(0, 32), (1, 33), (2, 34), (3, 35), (4, None), (5, None), (6, 36), (7, 37), (8, 38), (9, 39), (10, 40), (11, 41), (12, 42), (13, 43), (14, 44), (15, 45), (16, 46), (17, 47), (18, 48), (19, 49), (20, 50), (21, 51), (22, 52), (23, 53), (24, 54), (25, 55), (26, 56), (27, 57), (28, 58), (29, 59), (30, 60), (31, 61), (32, 62), (33, 63), (34, 64), (35, 65), (36, 66), (37, 67), (38, 68), (39, 69), (40, 70), (41, 71), (42, 72), (43, 73), (44, 74), (45, 75), (46, 76), (47, 77), (48, 78), (49, 79), (50, 80), (51, 81), (52, 82), (53, 83), (54, 84), (55, 85), (56, 86), (57, 87), (58, 88), (59, 89), (60, 90), (61, 91), (62, 92), (63, 93), (64, 94), (65, 95), (66, 96), (67, 97), (68, 98), (69, 99), (70, 100), (71, 101), (72, 102), (73, 103), (74, 104), (75, 105), (76, 106), (77, 107), (78, 108), (79, 109), (80, 110), (81, 111), (82, 112), (83, 113), (84, 114), (85, 115), (86, 116), (87, 117), (88, 118), (89, 119), (90, 120), (91, 121), (92, 122), (93, 123), (94, 124), (95, 125), (96, 126), (97, 127), (98, 128), (99, 129), (100, 130), (101, 131), (102, 132), (103, 133), (104, 134), (105, 135), (106, 136), (107, 137), (108, 138), (109, 139), (110, 140), (111, 141), (112, 142), (113, 143), (114, 144), (115, 145), (116, 146), (117, 147), (118, 148), (119, 149), (120, 150), (121, 151), (122, 152), (123, 153), (124, 154), (125, 155), (126, 156), (127, 157), (128, 158), (129, 159), (130, 160), (131, 161), (132, 162), (133, 163), (134, 164), (135, 165), (136, 166), (137, 167), (138, 168), (139, 169), (140, 170), (141, 171), (142, 172), (143, 173), (144, 174), (145, 175), (146, 176), (147, 177), (148, 178), (149, 179), (None, 180), (150, 181), (151, 182), (152, 183), (153, 184), (154, 185), (155, 186), (156, 187), (157, 188), (158, 189), (159, 190), (160, 191), (161, 192), (162, 193), (163, 194), (164, 195), (165, 196), (166, 197), (167, 198), (168, 199), (169, 200), (170, 201), (171, 202), (172, 203), (173, 204), (174, 205), (175, 206), (176, 207), (177, None), (178, 208), (179, 209), (180, 210), (181, 211), (182, 212), (183, 213), (184, 214), (185, 215), (186, 216), (187, 217), (188, 218), (189, 219), (190, 220), (191, 221), (192, 222), (193, 223), (194, 224), (195, 225), (196, 226), (197, 227), (198, 228), (199, 229), (200, 230), (201, 231), (202, 232), (203, 233), (204, 234), (205, 235), (206, 236), (207, 237), (208, 238), (209, 239), (210, None), (211, None), (212, None), (213, None), (214, None), (215, None), (216, None), (217, None), (218, None), (219, 240), (220, 241), (221, 242), (222, 243), (223, 244), (224, 245), (225, 246)]
        is_ngg = False

        inserter = Cas9IndicatorInserter(cutsite_index, pam_index, n20_pam_index, n20_index, aligned_pairs, is_ngg)

        reference_string, read_string = inserter.insert_indicators(reference, read)

        expected_reference = "ATTA__G---------------------------------" \
                             "----------------------------------------" \
                             "----------------------------------------" \
                             "-----------------------|CCT|AAG||GAAGTTT" \
                             "CAGCAAGGC|-CTA------TCT_G---CCA----CAGT-" \
                             "----GAG--GTC---T_________GACTCCC"
        expected_read = "GTTCGCG---------------------------------" \
                        "----------------------------------------" \
                        "----------------------------------------" \
                        "-----------------------|CCT|AAG||G_AGTTT" \
                        "CCAGAAGGC|-CCA------TTTGG---CAA----CGTT-" \
                        "----GGG--GCC---TGCCCCCCGGGATTGGG"

        self.assertEqual(reference_string, expected_reference)
        self.assertEqual(read_string, expected_read)

    def test_insert_indicators_to_ngg_array(self):
        reference_sequence = "GAC___G---------------------------------" \
                             "----------------------------------------" \
                             "--------TAGAGGGGCCGACGGAGATTAGG---------" \
                             "----------------------------------------" \
                             "----------------------------------------" \
                             "---------------------------"
        reference = list(reference_sequence)

        read_sequence = "TCCGCAG---------------------------------" \
                        "----------------------------------------" \
                        "--------TAGAGGGGCCGACGGAGA_TAGG---------" \
                        "----------------------------------------" \
                        "----------------------------------------" \
                        "---------------------------"
        read = list(read_sequence)

        cutsite_index = 115
        pam_index = 121
        n20_pam_index = 118
        n20_index = 98

        aligned_pairs = [(0, 14), (1, 15), (2, 16), (3, None), (4, None), (5, None), (6, 17), (7, 18), (8, 19), (9, 20), (10, 21), (11, 22), (12, 23), (13, 24), (14, 25), (15, 26), (16, 27), (17, 28), (18, 29), (19, 30), (20, 31), (21, 32), (22, 33), (23, 34), (24, 35), (25, 36), (26, 37), (27, 38), (28, 39), (29, 40), (30, 41), (31, 42), (32, 43), (33, 44), (34, 45), (35, 46), (36, 47), (37, 48), (38, 49), (39, 50), (40, 51), (41, 52), (42, 53), (43, 54), (44, 55), (45, 56), (46, 57), (47, 58), (48, 59), (49, 60), (50, 61), (51, 62), (52, 63), (53, 64), (54, 65), (55, 66), (56, 67), (57, 68), (58, 69), (59, 70), (60, 71), (61, 72), (62, 73), (63, 74), (64, 75), (65, 76), (66, 77), (67, 78), (68, 79), (69, 80), (70, 81), (71, 82), (72, 83), (73, 84), (74, 85), (75, 86), (76, 87), (77, 88), (78, 89), (79, 90), (80, 91), (81, 92), (82, 93), (83, 94), (84, 95), (85, 96), (86, 97), (87, 98), (88, 99), (89, 100), (90, 101), (91, 102), (92, 103), (93, 104), (94, 105), (95, 106), (96, 107), (97, 108), (98, 109), (99, 110), (100, 111), (101, 112), (102, 113), (103, 114), (104, 115), (105, 116), (None, 117), (106, 118), (107, 119), (108, 120), (109, 121), (110, 122), (111, 123), (112, 124), (113, 125), (114, 126), (115, 127), (116, 128), (117, 129), (118, 130), (119, 131), (120, 132), (121, 133), (122, 134), (123, 135), (124, 136), (125, 137), (126, 138), (127, 139), (128, 140), (129, 141), (130, 142), (131, 143), (132, 144), (133, 145), (134, 146), (135, 147), (136, 148), (137, 149), (138, 150), (139, 151), (140, 152), (141, 153), (142, 154), (143, 155), (144, 156), (145, 157), (146, 158), (147, 159), (148, 160), (149, 161), (150, 162), (151, 163), (152, 164), (153, 165), (154, 166), (155, 167), (156, 168), (157, 169), (158, 170), (159, 171), (160, 172), (161, 173), (162, 174), (163, 175), (164, 176), (165, 177), (166, 178), (167, 179), (168, 180), (169, 181), (170, 182), (171, 183), (172, 184), (173, 185), (174, 186), (175, 187), (176, 188), (177, 189), (178, 190), (179, 191), (180, 192), (181, 193), (182, 194), (183, 195), (184, 196), (185, 197), (186, 198), (187, 199), (188, 200), (189, 201), (190, 202), (191, 203), (192, 204), (193, 205), (194, 206), (195, 207), (196, 208), (197, 209), (198, 210), (199, 211), (200, 212), (201, 213), (202, 214), (203, 215), (204, 216), (205, 217), (206, 218), (207, 219), (208, 220), (209, 221), (210, 222), (211, 223), (212, 224), (213, 225), (214, 226), (215, 227), (216, 228), (217, 229), (218, 230), (219, 231), (220, 232), (221, 233), (222, 234), (223, 235), (224, 236), (225, 237)]
        is_ngg = True

        inserter = Cas9IndicatorInserter(cutsite_index, pam_index, n20_pam_index, n20_index, aligned_pairs, is_ngg)

        reference_string, read_string = inserter.insert_indicators(reference, read)

        expected_reference = "GAC___G---------------------------------" \
                             "----------------------------------------" \
                             "--------|TAGAGGGGCCGACGGAG||ATT|AGG|----" \
                             "----------------------------------------" \
                             "----------------------------------------" \
                             "--------------------------------"
        expected_read = "TCCGCAG---------------------------------" \
                        "----------------------------------------" \
                        "--------|TAGAGGGGCCGACGGAG||A_T|AGG|----" \
                        "----------------------------------------" \
                        "----------------------------------------" \
                        "--------------------------------"
        self.assertEqual(reference_string, expected_reference)
        self.assertEqual(read_string, expected_read)

    def test_apply_to_presentation_end_to_end(self):
        sequence = "GGATTCAGCACCCAGAATGAGGTGGTCTCTGAACGCCCCTCCTCCTTTACAGGCGAGGAAACAGCCCTGTGGGAAGTCGAGGTTCCAAGGTCACAGTGAGGGGGCCCTGGCCACCCGATTCAGCGCAGGAAATAGTGAGAAAGTCGTTTTTAGCCGACTCTGACCCGCATTCGGTTTCCAGTGCTGTCTTAGGAGGGCCGTGTGTTGAGGGTGGGCAAACGTGGTTTGGAGAGCG"
        n20 = "CCCGATTCAGCGCAGGAAAT"
        pam = "CCN"

        query_sequence = "TACCTTGGATTCAGCACCCAGAATGAGGTGGTCTCTGAACGCCCCTCCTCCTTTACAGGCGAGGAAACAGCCCTGTGGGAAGTCGAGGCTCCAAGGTCACAGTGAGGGGCCCTGGCCACCCGGATTCAGCGCAGGAAATAGTGAGAAAGTC"

        aligned_pairs = ((0, 1), (1, 2), (2, 3), (3, 4), (4, None), (5, None), (6, None), (7, None), (8, None), (9, None), (10, None), (11, 5), (12, 6), (13, 7), (14, 8), (15, 9), (16, 10), (17, 11), (18, 12), (19, 13), (20, 14), (21, 15), (22, 16), (23, 17), (24, 18), (25, 19), (26, 20), (27, 21), (28, 22), (29, 23), (30, 24), (31, 25), (32, 26), (33, 27), (34, 28), (35, 29), (36, 30), (37, 31), (38, 32), (39, 33), (40, 34), (41, 35), (42, 36), (43, 37), (44, 38), (45, 39), (46, 40), (47, 41), (48, 42), (49, 43), (50, 44), (51, 45), (52, 46), (53, 47), (54, 48), (55, 49), (56, 50), (57, 51), (58, 52), (59, 53), (60, 54), (61, 55), (62, 56), (63, 57), (64, 58), (65, 59), (66, 60), (67, 61), (68, 62), (69, 63), (70, 64), (71, 65), (72, 66), (73, 67), (74, 68), (75, 69), (76, 70), (77, 71), (78, 72), (79, 73), (80, 74), (81, 75), (82, 76), (83, 77), (84, 78), (85, 79), (86, 80), (87, 81), (88, 82), (89, 83), (90, 84), (91, 85), (92, 86), (93, 87), (94, 88), (95, 89), (96, 90), (97, 91), (98, 92), (99, 93), (100, 94), (101, 95), (102, 96), (103, 97), (104, 98), (None, 99), (105, 100), (106, 101), (107, 102), (108, 103), (109, 104), (110, 105), (111, 106), (112, 107), (113, 108), (114, 109), (115, 110), (116, 111), (117, 112), (118, 113), (119, 114), (120, 115), (121, None), (122, 116), (123, 117), (124, 118), (125, 119), (126, 120), (127, 121), (128, 122), (129, 123), (130, 124), (131, 125), (132, 126), (133, 127), (134, 128), (135, 129), (136, 130), (137, 131), (138, 132), (139, 133), (140, 134), (141, 135), (142, 136), (143, 137), (144, 138), (145, 139), (146, 140), (147, 141), (148, 142), (149, 143), (150, 144))

        reference_positions = [1, 2, 3, 4, None, None, None, None, None, None, None, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, None, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144]

        read = Read("foo", reference_positions, query_sequence, aligned_pairs)

        reference = Reference("test", n20, sequence, pam, [read])

        inserter = Cas9IndicatorInserter(reference.cutsite_index(),
                                      reference.pam_index(),
                                      reference.n20_pam_index(),
                                      reference.n20_index(),
                                      read.aligned_pairs,
                                      reference.is_ngg())

        processed_query_sequence = "TACCTTGGATTC---------------------------------------------------------------------------GCT--------------A_G---------CCACCCGGATTCAGCGCAGGAAAT------------"

        result_reference, result_read = inserter.insert_indicators(list(processed_query_sequence), list(processed_query_sequence))

        self.assertEqual(result_read, "TACCTTGGATTC---------------------------------------------------------------------------GCT--------------A_G---------|CCA|CCCG||GATTCAGCGCAGGAAAT|------------")

        p = Presenter([reference])
        results = p.present()
        mutation_clusters = results[0].mutation_clusters

        self.assertEqual(len(aligned_pairs) + 5, len(mutation_clusters[0].alignments[0].reference))

        self.assertTrue(mutation_clusters[0].cas9_region, "|CCA|CCCG||GATTCAGCGCAGGAAAT|")

class TestCas9IndicatorInserterWithPadding(unittest.TestCase):

    def create_aligned_pairs(self, read_sequence, reference_positions):
        return tuple(zip(range(len(read_sequence)), reference_positions))

    def test_apply_to_presentation(self):
        n20 = "ccccggggaaaa"
        sequence = "ttttttttttttttccccggggaaaacggttt"
        pam = "ngg"

        reference_positions_a = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
        sequence_a = "ttccccgggg"
        read_a = Read("foo", reference_positions_a, sequence_a, self.create_aligned_pairs(sequence_a, reference_positions_a))

        reference_positions_b = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
        sequence_b = "ttccccggggaaaacggtt"
        read_b = Read("bar", reference_positions_b, sequence_b, self.create_aligned_pairs(sequence_b, reference_positions_b))

        reference_positions_c = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        sequence_c = "ttccccgggga"
        read_c = Read("baz", reference_positions_c, sequence_c, self.create_aligned_pairs(sequence_c, reference_positions_c))

        reference_positions_d = [23, 24, 25, 26, 27]
        sequence_d = "aaacg"
        read_d = Read("bat", reference_positions_d, sequence_d, self.create_aligned_pairs(sequence_d, reference_positions_d))

        reference =  Reference("test", n20, sequence, pam, [read_a, read_b, read_c, read_d])

        inserter = Cas9IndicatorInserter(reference.cutsite_index(),
                                      reference.pam_index(),
                                      reference.n20_pam_index(),
                                      reference.n20_index(),
                                      read_a.aligned_pairs,
                                      reference.is_ngg())

        result_reference, result_read = inserter.insert_indicators(list(sequence_a), list(sequence_a))

        self.assertEqual(result_reference, "tt|ccccgggg?||")
        self.assertEqual(result_read, "tt|ccccgggg?||")

        inserter = Cas9IndicatorInserter(reference.cutsite_index(),
                                      reference.pam_index(),
                                      reference.n20_pam_index(),
                                      reference.n20_index(),
                                      read_b.aligned_pairs,
                                      reference.is_ngg())

        result_reference, result_read = inserter.insert_indicators(list(sequence_b), list(sequence_b))

        self.assertEqual(result_reference, "tt|ccccgggga||aaa|cgg|tt")
        self.assertEqual(result_read, "tt|ccccgggga||aaa|cgg|tt")

        inserter = Cas9IndicatorInserter(reference.cutsite_index(),
                                      reference.pam_index(),
                                      reference.n20_pam_index(),
                                      reference.n20_index(),
                                      read_c.aligned_pairs,
                                      reference.is_ngg())

        result_reference, result_read = inserter.insert_indicators(list(sequence_c), list(sequence_c))

        self.assertEqual(result_reference, "tt|ccccgggga||")
        self.assertEqual(result_read, "tt|ccccgggga||")

        inserter = Cas9IndicatorInserter(reference.cutsite_index(),
                                      reference.pam_index(),
                                      reference.n20_pam_index(),
                                      reference.n20_index(),
                                      read_d.aligned_pairs,
                                      reference.is_ngg())

        result_reference, result_read = inserter.insert_indicators(list(sequence_d), list(sequence_d))

        self.assertEqual(result_reference, "||aaa|cg")
        self.assertEqual(result_read, "||aaa|cg")

    def test_apply_to_presentation_for_ccn(self):
        n20 = "ccccggggaaaa"
        sequence = "aaacctccccggggaaaattt"
        pam = "ccn"

        reference_positions_a = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        sequence_a = "acctccccggggaaaat"
        read_a = Read("foo", reference_positions_a, sequence_a, self.create_aligned_pairs(sequence_a, reference_positions_a))

        reference_positions_b = [0, 1, 2, 3, 4, 5]
        sequence_b = "aaacct"
        read_b = Read("bar", reference_positions_b, sequence_b, self.create_aligned_pairs(sequence_b, reference_positions_b))

        reference_positions_c = [10, 11, 12, 13, 14, 15, 16, 17, 18]
        sequence_c = "ggggaaaat"
        read_c = Read("baz", reference_positions_c, sequence_c, self.create_aligned_pairs(sequence_c, reference_positions_c))

        reference =  Reference("test", n20, sequence, pam, [read_a, read_b, read_c])

        inserter = Cas9IndicatorInserter(reference.cutsite_index(),
                                      reference.pam_index(),
                                      reference.n20_pam_index(),
                                      reference.n20_index(),
                                      read_a.aligned_pairs,
                                      reference.is_ngg())

        result_reference, result_read = inserter.insert_indicators(list(sequence_a), list(sequence_a))

        self.assertEqual(result_reference, "a|cct|ccc||cggggaaaa|t")
        self.assertEqual(result_read, "a|cct|ccc||cggggaaaa|t")

        inserter = Cas9IndicatorInserter(reference.cutsite_index(),
                                      reference.pam_index(),
                                      reference.n20_pam_index(),
                                      reference.n20_index(),
                                      read_b.aligned_pairs,
                                      reference.is_ngg())

        result_reference, result_read = inserter.insert_indicators(list(sequence_b), list(sequence_b))

        self.assertEqual(result_reference, "aaa|cct???||")
        self.assertEqual(result_read, "aaa|cct???||")

        inserter = Cas9IndicatorInserter(reference.cutsite_index(),
                                      reference.pam_index(),
                                      reference.n20_pam_index(),
                                      reference.n20_index(),
                                      read_c.aligned_pairs,
                                      reference.is_ngg())

        result_reference, result_read = inserter.insert_indicators(list(sequence_c), list(sequence_c))

        self.assertEqual(result_reference, "||?ggggaaaa|t")
        self.assertEqual(result_read, "||?ggggaaaa|t")
