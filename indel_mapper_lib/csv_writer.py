import csv


class CsvWriter(object):
    def __init__(self, results):
        self.results = results

    def write_to(self, filename):
        with open(filename, "w") as file:
            writer = csv.writer(file)
            header = ["Name", "Total Reads", "Reference Cas9 Region", "Read Cas9 Region", "Description", "Count"]

            writer.writerow(header)
            for reference_presenter in self.results:
                self._write_reference(writer, reference_presenter)

    def _write_reference(self, writer, reference_presenter):
        prefix_cells = reference_presenter.csv_row_prefix_cells()
        if reference_presenter.has_mutation_clusters():
            for cluster in reference_presenter.mutation_clusters:
                writer.writerow(prefix_cells + cluster.csv_row())
        else:
            writer.writerow(prefix_cells)
