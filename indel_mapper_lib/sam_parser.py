from indel_mapper_lib.read import Read


class SamParser(object):

    def __init__(self, samfile):
        self.samfile = samfile

    def reference_name_to_reads_dict(self):
        result_dict = {}
        for filtered_pysam_read in filter(self.filter_bad_reads, self._fetch()):
            reference_name = filtered_pysam_read.reference_name
            new_read = self._make_read(filtered_pysam_read)
            if reference_name in result_dict:
                result_dict[reference_name].append(new_read)
            else:
                result_dict[reference_name] = [new_read]
        return result_dict

    def filter_bad_reads(self, pysam_read):
        try:
            pysam_read.reference_name  # try and see if the reference name exists
            return (len(pysam_read.get_reference_positions(full_length=True)) != 0) and \
                (pysam_read.query_sequence is not None)
        except:
            return False

    def _fetch(self):
        return self.samfile.fetch()

    def _make_read(self, pysam_read):
        return Read(query_name=pysam_read.query_name,
                    reference_positions=pysam_read.get_reference_positions(full_length=True),
                    query_sequence=pysam_read.query_sequence,
                    aligned_pairs=pysam_read.get_aligned_pairs())
