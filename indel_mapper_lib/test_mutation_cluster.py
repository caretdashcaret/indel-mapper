import unittest
from .alignment import Alignment
from .mutation_cluster import MutationCluster

class TestMutationCluster(unittest.TestCase):

    def test_mutation_cluster(self):
        alignment_a = Alignment(read="-aaa|a-",
                                reference="-aaa|t-")

        alignment_b = Alignment(read="-ccc|g-",
                                reference="-ccc|t-")

        cas9_region = Alignment(reference="caa", read="gta")

        cluster = MutationCluster(alignment_a, cas9_region)

        cluster.add_read(alignment_b)

        self.assertEqual(cluster.count(), 2)
        self.assertEqual(cluster.cas9_region.read, cas9_region.read)
        self.assertEqual(cluster.cas9_region.reference, cas9_region.reference)
        self.assertEqual(cluster.alignments[0].read, alignment_a.read)
        self.assertEqual(cluster.alignments[0].reference, alignment_a.reference)
        self.assertEqual(cluster.alignments[1].read, alignment_b.read)
        self.assertEqual(cluster.alignments[1].reference, alignment_b.reference)
        self.assertEqual(cluster.description, "2 mutations (ca to gt)")

        csv_row = cluster.csv_row()
        self.assertEqual(csv_row, [cas9_region.reference, cas9_region.read, "2 mutations (ca to gt)", 2])

    def test_has_mutations_adjacent_to_cutsite(self):
        alignment = Alignment(read="-A|GGG_||AAA|AGG|T-", reference="-A|GGGG||AAA|AGG|T-")
        cas9_region = Alignment(read="A|GGG_||AAA|AGG|T", reference="A|GGGG||AAA|AGG|T")
        cluster = MutationCluster(alignment, cas9_region)
        self.assertEqual(cluster.has_mutations_adjacent_to_cutsite(), True)

        alignment = Alignment(read="-A|GGGG||ATT|AGG|T-", reference="-A|GGGG||A_T|AGG|T-")
        cas9_region = Alignment(read="A|GGGG||ATT|AGG|T", reference="A|GGGG||A_T|AGG|T")
        cluster = MutationCluster(alignment, cas9_region)
        self.assertEqual(cluster.has_mutations_adjacent_to_cutsite(), False)

        alignment = Alignment(read="AAA|AGG|T--", reference="_AA|AGG|T--")
        cas9_region = Alignment(read="AAA|AGG|T", reference="_AA|AGG|T")
        cluster = MutationCluster(alignment, cas9_region)
        self.assertEqual(cluster.has_mutations_adjacent_to_cutsite(), True)

        alignment = Alignment(read="--A|CCA|AA_", reference="--A|CCA|AAA")
        cas9_region = Alignment(read="A|CCA|AA_", reference="A|CCA|AAA")
        cluster = MutationCluster(alignment, cas9_region)
        self.assertEqual(cluster.has_mutations_adjacent_to_cutsite(), True)

        alignment = Alignment(read="--A|CCA|AAG", reference="--A|CCA|AAA")
        cas9_region = Alignment(read="A|CCA|AAG", reference="A|CCA|AAA")
        cluster = MutationCluster(alignment, cas9_region)
        self.assertEqual(cluster.has_mutations_adjacent_to_cutsite(), True)

    def test_to_dict(self):
        alignment_a = Alignment(read="-aaa|a-",
                                reference="-aaa|t-")

        alignment_b = Alignment(read="-ccc|g-",
                                reference="-ccc|t-")

        cas9_region = Alignment(reference="caa", read="gta")

        cluster = MutationCluster(alignment_a, cas9_region)

        cluster.add_read(alignment_b)

        self.assertEqual(cluster.to_dict(),
                         {
                             "cas9_region": {"reference": "caa", "read": "gta"},
                             "count": 2,
                             "description": "2 mutations (ca to gt)",
                             "alignments": [{"reference":"-aaa|t-", "read":"-aaa|a-"}, {"reference":"-ccc|t-", "read":"-ccc|g-"}]
                         }
        )
