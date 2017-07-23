from .sequence_diff import SequenceDiff


class Alignment(object):
    def __init__(self, reference, read):
        self.reference = reference
        self.read = read

    def description(self):
        return SequenceDiff(self.reference, self.read).description()

    def has_unmatched_bases_at(self, index):
        return self.reference[index] != self.read[index]

    def starts_with(self, alignment):
        return self.read.startswith(alignment.read) and self.reference.startswith(alignment.reference)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (other.reference == self.reference and
                    other.read == self.read)
        return False

    def __repr__(self):
        return "({}, {})".format(self.reference, self.read)

    def to_dict(self):
        return {
            "read": self.read,
            "reference": self.reference,
        }
