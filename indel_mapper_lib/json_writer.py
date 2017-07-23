import json


class JsonWriter(object):
    def __init__(self, results):
        self.results = results

    def write_to(self, filename):
        json_file = open(filename, "w")
        json_file.write(json.dumps([result.to_dict() for result in self.results]))

    def _write_reference(self, writer, reference_presenter):
        prefix_cells = reference_presenter.csv_row_prefix_cells()
        if reference_presenter.has_mutation_clusters():
            for cluster in reference_presenter.mutation_clusters:
                writer.writerow(prefix_cells + cluster.csv_row())
        else:
            writer.writerow(prefix_cells)
