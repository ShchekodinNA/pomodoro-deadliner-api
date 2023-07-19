from enum import Enum


class PomodoroBaseEnum(Enum):
    LONG_REST = 15
    SHORT_REST = 5
    WORK = 25
    ITERATIONS = 4
