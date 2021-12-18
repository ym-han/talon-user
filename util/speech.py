from user.util.talon import active_list
import re

RE_SNAKE = r"(?<![A-Za-z])([A-Z]?[a-z]+)"
RE_CAMEL = r"(?<=[A-Za-z])([A-Z][a-z]*)"
RE_NUM = r"([0-9])"
RE_WORD = re.compile(f"{RE_SNAKE}|{RE_CAMEL}|{RE_NUM}")


def create_spoken_form(text: str) -> str:
    ALPHABET = active_list("user.key_alphabet")
    DIGITS = active_list("user.key_number")
    chunks = RE_WORD.finditer(text)
    chunks = [m.group(0) for m in chunks]
    chunks = list(map(str.lower, chunks))
    for k, v in enumerate(chunks):
        if v in ALPHABET:
            chunks[k] = ALPHABET[v]
        if v in DIGITS:
            chunks[k] = DIGITS[v]
    spoken_form = " ".join(chunks)
    return spoken_form

# assert create_spoken_form("user.get_match1") == "user get match one"
# assert create_spoken_form("user.macro_play") == "user macro play"
# assert create_spoken_form("BlockingIOError") == "blocking sit odd error"