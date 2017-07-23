from .mutation_cluster import MutationCluster

class ReferencePresenter(object):
    def __init__(self, reference, mutation_clusters):
        self.mutation_clusters = mutation_clusters
        self._name = reference.name
        self._sequence = reference.sequence
        self._n20 = reference.n20
        self._pam = reference.pam
        self._total_reads = len(reference.reads)

    def name(self):
        return self._name

    def sequence(self):
        return self._sequence

    def n20(self):
        return self._n20

    def pam(self):
        return self._pam

    def has_mutation_clusters(self):
        return len(self.mutation_clusters) != 0

    def total_reads(self):
        return self._total_reads

    def csv_row_prefix_cells(self):
        return [self.name(), self.total_reads()]

    def to_dict(self):
        return {
            "name": self.name(),
            "sequence": self.sequence(),
            "n20": self.n20(),
            "pam": self.pam(),
            "has_mutation_clusters": self.has_mutation_clusters(),
            "total_reads": self.total_reads(),
            "mutation_clusters": [cluster.to_dict() for cluster in self.mutation_clusters]
        }
