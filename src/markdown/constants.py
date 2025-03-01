import re

HEADING_PATTERN = re.compile(
    r"^(?P<marker>\#{1,6})\ "  # Captures inside a named capture group
    r"(?P<content>.+)$",  # and the content
    flags=re.VERBOSE,
)
CODE_PATTERN = re.compile(
    r"^```\n"
    r"(?P<content>.*?)"  # Captures inside a named capture group
    r"\n?```$",
    flags=re.VERBOSE | re.DOTALL,
)
QUOTE_PATTERN = re.compile(
    r"^>\ (?P<content>.+)$",  # Captures inside a named capture group
    flags=re.VERBOSE,
)
UNORDERED_LIST_PATTERN = re.compile(
    r"^[\*-]\ (?P<content>.+)$",  # Capture inside a named capture group
    flags=re.VERBOSE | re.MULTILINE,
)
ORDERED_LIST_PATTERN = re.compile(
    r"^(?P<number>[0-9]+)"  # Captures inside a named capture group
    r"\.\ "
    r"(?P<content>.+)$",  # and the content
    flags=re.VERBOSE | re.MULTILINE,
)
