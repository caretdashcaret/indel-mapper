from .reference_presenter import ReferencePresenter
from .reference_processor import ReferenceProcessor

class Presenter(object):
    def __init__(self, references):
        self.references = references

    def present(self):
        processor = ReferenceProcessor()
        results = []
        for reference in self.references:
            if reference.has_reads_with_indels_near_the_cutsite:
                mutation_clusters = processor.compute_mutation_clusters(reference)
                results.append(ReferencePresenter(reference, mutation_clusters))
        return results
