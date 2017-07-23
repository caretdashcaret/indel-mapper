class Sequence:
    """A sequence of DNA base pairs."""

    BASE_MAPPING = {
        "A": "T",
        "C": "G",
        "G": "C",
        "T": "A",
    }

    def __init__(self, contents):
        """Instantiate and validate a new Sequence."""
        self.contents = contents.upper()
        self._validate()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.contents == other.contents
        return False

    def __str__(self):
        return self.contents

    def reverse_complement(self):
        """Return a new Sequence containing the reverse complement of the original
        sequence."""
        rc_bases = [self.BASE_MAPPING[base] for base in self.contents][::-1]
        return Sequence("".join(rc_bases))

    def _validate(self):
        for base in self.contents:
            if self._unknown_base(base):
                raise ValueError("Unknown base: \"%s\"", base)

    def _unknown_base(self, base):
        return base not in self.BASE_MAPPING
