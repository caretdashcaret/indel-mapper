import unittest
from .read import Read
from .alignment import Alignment
from .reference import Reference
from .presenter import Presenter

class TestPresenter(unittest.TestCase):

    def create_aligned_pairs(self, read_sequence, reference_positions):
        return tuple(zip(range(len(read_sequence)), reference_positions))

    def create_test_reference(self, name):
        self.n20 = "aaaatttc"
        self.sequence = "tactactacaaaatttccggt"
        self.pam = "ngg"

        reference_positions_a = [8, None, None, None, 9, 10, 11, None, None, None, None, 12, 13, 14]
        seq_a = "ctttaaattttatt"
        read_a = Read("a", reference_positions_a, seq_a, self.create_aligned_pairs(seq_a, reference_positions_a))

        reference_positions_b = [10, 15]
        seq_b = "at"
        read_b = Read("b", reference_positions_b, seq_b, ((0,10),(None, 11), (None, 12), (None, 13), (None, 14), (1, 15)))

        reference_positions_c = [10, 11, 12, 13, 14]
        seq_c = "aaatt"
        read_c = Read("c", reference_positions_c, seq_a, self.create_aligned_pairs(seq_c, reference_positions_c))

        reference_positions_d = [6, 7, 8, 9, 10, 11, 12, 13, None, None, None, None, 14]
        seq_d = "tacaaaattggggt"
        read_d = Read("d", reference_positions_d, seq_d, self.create_aligned_pairs(seq_d, reference_positions_d))

        reference_positions_e = [18, 20]
        seq_e = "gt"
        read_e = Read("e", reference_positions_e, seq_e, ((0,18),(None, 19),(1,20)))

        reference_positions_f = [None, None, None, 0, 1, 2]
        seq_f = "gggtac"
        read_f = Read("f", reference_positions_f, seq_f, self.create_aligned_pairs(seq_f, reference_positions_f))

        reads = [read_a, read_b, read_c, read_d, read_e, read_f]

        return Reference(name, self.n20, self.sequence, self.pam, reads)

    def test_reference_presenter_results(self):

        references = [self.create_test_reference("foo"), self.create_test_reference("bar")]

        test_presenter = Presenter(references)
        results = test_presenter.present()

        self.assertEqual(len(results), 2)

        self.assertEqual(results[0].sequence(), self.sequence.upper())
        self.assertEqual(results[0].n20(), self.n20.upper())
        self.assertEqual(results[0].pam(), self.pam.upper())
        self.assertEqual(results[0].name(), "foo")
        self.assertEqual(len(results[0].mutation_clusters), 1)
        self.assertEqual(results[0].total_reads(), 6)

        self.assertEqual(results[1].sequence(), self.sequence.upper())
        self.assertEqual(results[1].n20(), self.n20.upper())
        self.assertEqual(results[1].pam(), self.pam.upper())
        self.assertEqual(results[1].name(), "bar")
        self.assertEqual(len(results[1].mutation_clusters), 1)
        self.assertEqual(results[1].total_reads(), 6)

    def test_cluster_results(self):
        references = [self.create_test_reference("foo")]

        test_presenter = Presenter(references)
        results = test_presenter.present()

        mutation_clusters = results[0].mutation_clusters

        self.assertEqual(mutation_clusters[0].count(), 1)

        expected = [('A___||_T', 'A___||_T', 'AAAT||TT')]

        actual = []
        for cluster in mutation_clusters:
            got = (cluster.cas9_region.read, cluster.alignments[0].read, cluster.alignments[0].reference)
            actual.append(got)

        self.assertEqual(sorted(expected), sorted(actual))
