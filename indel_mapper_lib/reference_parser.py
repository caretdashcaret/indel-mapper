from indel_mapper_lib.reference import Reference


class ReferenceParser():

    def __init__(self, reference_file, reference_name_to_reads):
        self.reference_file = reference_file
        self.reference_name_to_reads = reference_name_to_reads

    def references(self):
        references_from_file = []

        for line in self.reference_file:
            name, n20, sequence, pam = line
            reads_for_reference = self._reads_for_reference(name)
            references_from_file.append(Reference(name=name.strip(),
                                                  n20=n20.strip(),
                                                  sequence=sequence.strip(),
                                                  pam=pam.strip(),
                                                  reads=reads_for_reference))

        return references_from_file

    def _reads_for_reference(self, reference_name):
        if reference_name in self.reference_name_to_reads:
            return self.reference_name_to_reads[reference_name]
        return []
