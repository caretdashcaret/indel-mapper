from indel_mapper_lib.indel import Indel


class Read(object):

    def __init__(self, query_name, reference_positions, query_sequence, aligned_pairs):
        self.query_name = query_name
        self.query_sequence = query_sequence.upper()
        self.aligned_pairs = tuple(aligned_pairs)
        self.indels = []
        self.valid_indels = []

        self._compute_indels(reference_positions)

    def _compute_indels(self, reference_positions):
        # self.reference_positions is an array of indexes that signify how the
        # read aligns to the reference.

        # Example 1: [120, 121, None, None, None, 122]

        # This indicates the read has 2 bases that matches the 120th and 121st
        # base of the reference sequence. The 'None's indicate the read then has
        # 3 additional bases that the reference doesn't have. Then the read has
        # a base that matches the reference again. This would be an insertion.

        # Example 2: [120, 121, 125]

        # This indicates that the read has 2 bases that matches the 120th and
        # 121st base of the reference sequence. However, the read is missing 3
        # bases that would otherwise match the 122th, 123th, and 124th base of
        # the reference sequence. It has another base that matches the 125th of
        # the reference sequence. This would be an deletion.

        prev_reference_index = reference_positions[0]
        reference_index_of_start_of_insertion = reference_positions[0]
        indel_length = 0

        for reference_index in reference_positions[1:]:
            if reference_index is not None:
                if prev_reference_index is not None:
                    # deletion
                    if reference_index != prev_reference_index + 1 and reference_index != prev_reference_index:
                        self._make_new_indel(start_index=prev_reference_index,
                                             end_index=reference_index,
                                             length=((reference_index-1) - prev_reference_index),
                                             is_deletion=True)
                else:
                    # end of insertion (previous reference_index is None and current is not None)
                    self._make_new_indel(start_index=reference_index_of_start_of_insertion,
                                         end_index=reference_index,
                                         length=indel_length,
                                         is_deletion=False)
                    indel_length = 0
            else:
                # start of insertion
                if prev_reference_index is not None:
                    reference_index_of_start_of_insertion = prev_reference_index
                    indel_length += 1
                else:
                    indel_length += 1

            prev_reference_index = reference_index

    def _make_new_indel(self, start_index, end_index, length, is_deletion):
        new_indel = Indel(start_index=start_index,
                          end_index=end_index,
                          length=length,
                          is_deletion=is_deletion)
        self.indels.append(new_indel)
        if new_indel.is_valid:
            self.valid_indels.append(new_indel)
