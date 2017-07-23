from .alignment import Alignment

class Realigner:
    def __init__(self, alignment):
        self.alignment = alignment

    def align(self):
        left_ref, right_ref = self.alignment.reference.split("||")
        left_read, right_read = self.alignment.read.split("||")

        # Push underscores toward the insertion site in the read.
        new_left_read = self._shift_left(left_ref, list(left_read))
        new_right_read = self._shift_left(right_ref[::-1], list(right_read[::-1]))[::-1]

        # Push underscores toward the insertion site in the reference.
        new_left_ref = self._shift_left(new_left_read, list(left_ref))
        new_right_ref = self._shift_left(new_right_read[::-1], list(right_ref[::-1]))[::-1]

        return Alignment(new_left_ref + "||" + new_right_ref,
                         new_left_read + "||" + new_right_read)

    def _shift_left(self, ref, read):
        # For every base in the sequence,
        for i, base in enumerate(read):
            # if it's preceded by an underscore,
            if i != 0 and read[i - 1] == "_" and read[i] != "_":
                j = i - 1
                # search backward to find where the chain of underscores began,
                while read[j] == "_":
                    j -= 1
                j += 1
                # then find the leftmost position the base matches, and move it there.
                while j < i:
                    if ref[j] == base:
                        read[j] = base
                        read[i] = "_"
                        break
                    j += 1
        return "".join(read)
