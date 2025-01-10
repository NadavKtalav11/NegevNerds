from enum import Enum

class Moed(Enum):
    A = "א"
    B = "ב"
    C = "ג"
    D = "ד"

    def __str__(self):
        return self.value

class Semester(Enum):
    FALL = "סתיו"
    SPRING = "אביב"
    SUMMER = "קיץ"

    def __str__(self):
        return self.value