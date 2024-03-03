import re

def size_to_percent(size):
    if size == "LARGE":
        return 1.0
    if size == "MEDIUM":
        return 0.5
    if size == "SMALL":
        return 0.25
    return -1