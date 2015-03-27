
class InvalidScoresheetException(Exception):
    pass

MAX_FLAGS = 5

class Scorer:
    def __init__(self, scoresheet):
        self._scoresheet = scoresheet

    def calculate_scores(self):
        scores = {}
        for tla, data in self._scoresheet.items():
            flags = data['flags']
            self._check_num_flags(tla, flags)
            scores[tla] = flags
        return scores

    def validate(self, extra):
        total_flags = 0

        for tla, data in self._scoresheet.items():
            flags = data['flags']
            self._check_num_flags(tla, flags)
            total_flags += flags

        if extra is not None:
            unclaimed_flags = extra['unclaimed_flags']
            self._check_num_flags('unclaimed_flags', unclaimed_flags)
            total_flags += unclaimed_flags

        if total_flags != MAX_FLAGS:
            msg = "Wrong overall number of flags (expecting {0}, got {1})" \
                    .format(total_flags, MAX_FLAGS)
            raise InvalidScoresheetException(msg)

    def _check_num_flags(self, who, flags):
        if not isinstance(flags, int):
            msg = "{0} has invalid flags value ({1}, expected int)" \
                    .format(who, repr(flags))
            raise InvalidScoresheetException(msg)

        if flags > MAX_FLAGS:
            msg = "{0} has too many flags ({1}; max: {2})" \
                    .format(who, flags, MAX_FLAGS)
            raise InvalidScoresheetException(msg)

        if flags < 0:
            msg = "{0} has negative flags! ({1})".format(who, flags)
            raise InvalidScoresheetException(msg)
