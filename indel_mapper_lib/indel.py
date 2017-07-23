class Indel(object):

    def __init__(self, start_index, end_index, length, is_deletion):
        self.start_index = start_index
        self.end_index = end_index
        self.length = length
        self.is_deletion = is_deletion
        self.is_insertion = not is_deletion
        self.is_valid = self._is_valid()

    def is_enveloping_cutsite(self, cutsite_index):
        return self.start_index <= cutsite_index and self.end_index >= cutsite_index

    def _is_valid(self):
        return self.start_index is not None and self.end_index is not None
