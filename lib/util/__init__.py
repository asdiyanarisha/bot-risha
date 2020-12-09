
import re


class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]


newline_spliter_re_ = re.compile("\n\n|\r\n|\n\r|\n")


def split_to_paragraphs(text):
    """Split whole text into paragraphs
    """
    paragraphs = [a.strip() for a in newline_spliter_re_.split(text) if a.strip() != ""]
    return paragraphs


