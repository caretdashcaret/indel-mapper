class Cas9IndicatorInserter(object):
    def __init__(self, cutsite_index, pam_index, n20_pam_index, n20_index, aligned_pairs, is_ngg):
        self.cutsite_index = cutsite_index
        self.pam_index = pam_index
        self.n20_pam_index = n20_pam_index
        self.n20_index = n20_index
        self.aligned_pairs = aligned_pairs
        self.is_ngg = is_ngg
        self.cas9_indicators = self._cas9_indicators()

    def _cas9_indicators(self):
        cas9_indicators = {}
        for aligned_pair_index, sequence_indexes in enumerate(self.aligned_pairs):
            _, reference_index = sequence_indexes
            if reference_index == self.cutsite_index:
                cas9_indicators["cutsite"] = aligned_pair_index
            elif reference_index == self.pam_index:
                cas9_indicators["pam"] = aligned_pair_index
            elif reference_index == self.n20_pam_index:
                cas9_indicators["n20_pam"] = aligned_pair_index
            elif reference_index == self.n20_index:
                cas9_indicators["n20"] = aligned_pair_index
        return cas9_indicators

    def _read_is_right_of_cutsite(self):
        return self._distance_of_right_read_to_cutsite() > 0

    def _read_is_left_of_cutsite(self):
        return self._distance_of_left_read_to_cutsite() > 0

    def _distance_of_right_read_to_cutsite(self):
        for _, reference_index in self.aligned_pairs:
            if reference_index is not None:
                return reference_index - self.cutsite_index

    def _distance_of_left_read_to_cutsite(self):
        for _, reference_index in reversed(self.aligned_pairs):
            if reference_index is not None:
                return self.cutsite_index - reference_index

    def insert_indicators(self, reference_presentation_array, read_presentation_array):
        reference_presentation_string = ''
        read_presentation_string = ''
        if len(self.cas9_indicators) > 0:
            for index, value in enumerate(reference_presentation_array):
                already_added = False

                for cas9_mark, cas9_mark_index in self.cas9_indicators.items():
                    if index == cas9_mark_index:
                        if self.is_ngg:
                            reference_presentation_string += value + self._get_marking(cas9_mark)
                            read_presentation_string += read_presentation_array[index] + self._get_marking(cas9_mark)
                        else:
                            reference_presentation_string += self._get_marking(cas9_mark) + value
                            read_presentation_string += self._get_marking(cas9_mark) + read_presentation_array[index]
                        already_added = True

                if not already_added:
                    reference_presentation_string += value
                    read_presentation_string += read_presentation_array[index]

        else:
            reference_presentation_string = ''.join(reference_presentation_array)
            read_presentation_string = ''.join(read_presentation_array)

        return self._pad_strings_if_needed(reference_presentation_string, read_presentation_string)

    def _pad_strings_if_needed(self, reference_presentation_string, read_presentation_string):
        if self._read_is_right_of_cutsite():
            padding = "||" + "?" * self._get_padding_length_for_right_read()
            reference_presentation_string = padding + reference_presentation_string
            read_presentation_string = padding + read_presentation_string
        elif self._read_is_left_of_cutsite():
            padding = "?" * self._get_padding_length_for_left_read() + "||"
            reference_presentation_string = reference_presentation_string + padding
            read_presentation_string = read_presentation_string + padding
        return reference_presentation_string, read_presentation_string

    def _get_padding_length_for_right_read(self):
        if self.is_ngg:
            return self._distance_of_right_read_to_cutsite() - 1
        else:
            return self._distance_of_right_read_to_cutsite()

    def _get_padding_length_for_left_read(self):
        if self.is_ngg:
            return self._distance_of_left_read_to_cutsite()
        else:
            return self._distance_of_left_read_to_cutsite() - 1

    def _get_marking(self, cas9_mark):
        if cas9_mark == "cutsite":
            return "||"
        else:
            return "|"
