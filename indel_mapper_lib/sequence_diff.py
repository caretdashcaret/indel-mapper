from enum import Enum

from .diff_components import DiffDeletion
from .diff_components import DiffInsertion
from .diff_components import DiffMatch
from .diff_components import DiffMutation


class DiffState(Enum):
    DELETION = 1
    INSERTION = 2
    MATCH = 3
    MUTATION = 4


class SequenceDiff(object):
    STATE_MAP = {
        DiffState.DELETION: DiffDeletion,
        DiffState.INSERTION: DiffInsertion,
        DiffState.MATCH: DiffMatch,
        DiffState.MUTATION: DiffMutation,
    }

    def __init__(self, original, changed):
        self._validate(original, changed)
        self.changes = self._change_tokens(original, changed)

    def description(self):
        without_trailing_matches = self._strip_end_matches(self.changes)
        return ", ".join([str(change) for change in without_trailing_matches])

    def _change_tokens(self, original, changed):
        curr_ref = ""
        curr_read = ""
        state = DiffState.MATCH
        tokens = []

        # Compare each pair of bases
        for base_1, base_2 in zip(original, changed):
            # Skip metadata (like | and ||)
            if base_1 == "|" and base_2 == "|":
                pass

            # Begin/continue reading a DiffMatch
            elif base_1 == base_2:
                if state == DiffState.MATCH:
                    curr_ref += base_1
                    curr_read += base_2
                else:
                    tokens.append(self._create_diff(curr_ref, curr_read, state))
                    curr_ref = base_1
                    curr_read = base_2
                    state = DiffState.MATCH

            # Begin/continue reading a DiffInsertion
            elif base_1 == "_":
                if state == DiffState.INSERTION:
                    curr_ref += base_1
                    curr_read += base_2
                else:
                    tokens.append(self._create_diff(curr_ref, curr_read, state))
                    curr_ref = base_1
                    curr_read = base_2
                    state = DiffState.INSERTION

            # Begin/continue reading a DiffDeletion
            elif base_2 == "_":
                if state == DiffState.DELETION:
                    curr_ref += base_1
                    curr_read += base_2
                else:
                    tokens.append(self._create_diff(curr_ref, curr_read, state))
                    curr_ref = base_1
                    curr_read = base_2
                    state = DiffState.DELETION

            # If the bases don't match, this must be a DiffMutation
            else:
                if state == DiffState.MUTATION:
                    curr_ref += base_1
                    curr_read += base_2
                else:
                    tokens.append(self._create_diff(curr_ref, curr_read, state))
                    curr_ref = base_1
                    curr_read = base_2
                    state = DiffState.MUTATION

        # Append the last token
        if curr_read != "":
            tokens.append(self._create_diff(curr_ref, curr_read, state))

        return tokens

    def _create_diff(self, ref_seq, read_seq, state):
        if state in self.STATE_MAP:
            return self.STATE_MAP[state](ref_seq, read_seq)
        else:
            raise ValueError("Unknown diff state \"{}\"".format(state))

    def _validate(self, original, changed):
        if len(original) != len(changed):
            raise ValueError("Can't diff sequences of differing length")
        if self._cutsite_positions(original) != self._cutsite_positions(changed):
            raise ValueError("Can't diff sequences with misaligned cutsites")

    def _cutsite_positions(self, seq):
        return [pos for pos, base in enumerate(seq) if base == "|"]

    def _strip_end_matches(self, changes):
        while len(changes) != 0 and changes[0].is_match():
            changes = changes[1:]
        while len(changes) != 0 and changes[-1].is_match():
            changes = changes[:-1]
        return changes
