from enum import Enum

class Certainty(Enum):
    CERTAIN = 1
    NEARLY_CERTAIN = 2
    VERY_LIKELY = 3
    LIKELY = 4
    EITHER = 5
    UNLIKELY = 6
    VERY_UNLIKELY = 7
    NEARLY_IMPOSSIBLE = 8
    IMPOSSIBLE = 9