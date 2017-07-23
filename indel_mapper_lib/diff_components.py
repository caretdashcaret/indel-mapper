class DiffComponent(object):
    def __init__(self, ref_seq, read_seq):
        if len(ref_seq) != len(read_seq):
            raise ValueError("Reference {} and read {} should be the same length".format(ref_seq, read_seq))
        self.ref_seq = ref_seq
        self.read_seq = read_seq

    def is_match(self):
        return False

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                other.ref_seq == self.ref_seq and
                other.read_seq == self.read_seq)

    def _size(self):
        return len(self.read_seq)


class DiffMatch(DiffComponent):
    def is_match(self):
        return True

    def __repr__(self):
        name = "match"
        if self._size() > 1:
            name = "matches"
        return "{} {}".format(self._size(), name)


class DiffInsertion(DiffComponent):
    def __repr__(self):
        name = "insertion"
        if self._size() > 1:
            name = "insertions"
        return "{} {} ({})".format(self._size(), name, self.read_seq)


class DiffDeletion(DiffComponent):
    def __repr__(self):
        name = "deletion"
        if self._size() > 1:
            name = "deletions"
        return "{} {} ({})".format(self._size(), name, self.ref_seq)


class DiffMutation(DiffComponent):
    def __repr__(self):
        name = "mutation"
        if self._size() > 1:
            name = "mutations"
        return "{} {} ({} to {})".format(self._size(), name, self.ref_seq,
                                         self.read_seq)
