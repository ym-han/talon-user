from __future__ import annotations
from itertools import chain, repeat
from typing import Any, Callable, Iterable, Optional, Sequence, Union
from talon import Module, Context, actions, imgui, ui
from talon.grammar.vm import Phrase

import re

mod = Module()
ctx = Context()

# NOTE: This is different from the definition of a camelCase boundary
#       in create_spoken_form: this one splits "IOError" as "IO Error",
#       whereas the other splits it as "I O Error", which is important
#       when creating a spoken form as each capitalized letter should
#       be pronounced separately, but which would reformat "IOError"
#       as i_o_error in snake_case.
REGEX_CAMEL_BOUNDARY = re.compile(
    "|".join(
        (
            r"(?<=[a-z])(?=[A-Z])",
            r"(?<=[A-Z])(?=[A-Z][a-z])",
            r"(?<=[A-Za-z])(?=[0-9])",
            r"(?<=[0-9])(?=[A-Za-z])",
        )
    )
)

# NOTE: A delimiter char followed by a blank space is no delimiter.
REGEX_DELIMITER = re.compile(r"[-_.:/](?!\s)+")


class ImmuneString(object):
    """Wrapper that makes a string immune from formatting."""

    def __init__(self, string):
        self.string = string


@mod.capture(rule="({user.key_symbol_immune} | <user.number_prefix>)")
def immune_string(m) -> ImmuneString:
    return ImmuneString(str(m[0]))


Chunk = Union[str, ImmuneString]
StringFormatter = Callable[[str], str]


class Formatter(object):
    @staticmethod
    def from_description(formatter_names: str) -> Formatter:
        global FORMATTERS_DICT
        formatter = Formatter()
        for formatter_name in formatter_names.split(","):
            formatter += FORMATTERS_DICT[formatter_name]
        return formatter

    def __init__(
        self,
        delimiter: Optional[str] = None,
        chunk_formatters: Sequence[Optional[StringFormatter]] = (None,),
        string_formatters: Sequence[StringFormatter] = (),
    ):
        self.__delimiter = delimiter
        self.chunk_formatters = tuple(chunk_formatters)
        self.string_formatters = tuple(string_formatters)

    def __repr__(self):
        result = "{\n"
        result += f"  delimiter = '{self.delimiter()}',\n"
        for i, chunk_formatter in enumerate(self.chunk_formatters):
            sample = "sample"
            if chunk_formatter:
                sample = chunk_formatter(sample)
            result += f"  chunk_formatter({i}, 'sample') = '{sample}',\n"
        for i, string_formatter in enumerate(self.string_formatters):
            sample = "sample"
            if string_formatter:
                sample = string_formatter(sample)
            result += f"  string_formatter({i}, 'sample') = '{sample}',\n"
        result += "}"
        return result

    @staticmethod
    def pick_delimiter(delimiter1: Optional[str], delimiter2: Optional[str]):
        return delimiter2 if delimiter1 is None else delimiter1

    def __add__(self, other: Formatter) -> Formatter:
        return Formatter(
            Formatter.pick_delimiter(other.__delimiter, self.__delimiter),
            other.chunk_formatters or self.chunk_formatters,
            other.string_formatters + self.string_formatters,
        )

    def delimiter(self) -> str:
        return " " if self.__delimiter is None else self.__delimiter

    def string_formatter(self, string: str) -> str:
        for string_formatter in self.string_formatters:
            string = string_formatter(string)
        return string

    def chunk_formatter_chain(self) -> Iterable[Optional[StringFormatter]]:
        repeat_last = repeat(self.chunk_formatters[-1])
        return chain(self.chunk_formatters, repeat_last)

    def __call__(self, chunks: Sequence[Chunk]):
        formatted_string = ""
        shifted_chunks = chain(chunks[1:], [None])
        for chunk_formatter, curr_chunk, next_chunk in zip(
            self.chunk_formatter_chain(), chunks, shifted_chunks
        ):
            curr_chunk_is_last = next_chunk is None
            curr_chunk_is_immune = isinstance(curr_chunk, ImmuneString)
            next_chunk_is_immune = isinstance(next_chunk, ImmuneString)

            if curr_chunk_is_immune:
                formatted_string += curr_chunk.string
            else:
                if chunk_formatter:
                    formatted_string += chunk_formatter(curr_chunk)
                else:
                    formatted_string += curr_chunk
                if not (curr_chunk_is_last or next_chunk_is_immune):
                    formatted_string += self.delimiter()

        return self.string_formatter(formatted_string)


def FormatTopLevel(prefix: str = "", suffix: str = "") -> Formatter:
    return Formatter(string_formatters=(lambda text: f"{prefix}{text}{suffix}",))


def FormatChunk(chunk_formatters: list[Optional[StringFormatter]]) -> Formatter:
    return Formatter(chunk_formatters=chunk_formatters)


def JoinBy(delimiter: str) -> Formatter:
    return Formatter(delimiter=delimiter)


FORMATTERS_DICT = {
    "NOOP": Formatter(),
    "TRAILING_PADDING": FormatTopLevel(suffix=" "),
    "TRAILING_QUESTION_MARK": FormatTopLevel(suffix="?"),
    "TRAILING_EXCLAMATION_MARK": FormatTopLevel(suffix="!"),
    "LEADING_SINGLE_DASH": FormatTopLevel(prefix="-"),
    "LEADING_DOUBLE_DASH": FormatTopLevel(prefix="--"),
    "DOUBLE_QUOTED_STRING": FormatTopLevel(prefix='"', suffix='"'),
    "SINGLE_QUOTED_STRING": FormatTopLevel(prefix="'", suffix="'"),
    "ALL_UPPERCASE": FormatChunk([str.upper]),
    "ALL_LOWERCASE": FormatChunk([str.lower]),
    "CAPITALIZE_ALL": FormatChunk([str.capitalize]),
    "CAPITALIZE_FIRST": FormatChunk([str.capitalize, None]),
    "CAPITALIZE_REST": FormatChunk([None, str.capitalize]),
    "SNAKE_CASE": JoinBy("_"),
    "DASH_SEPARATED": JoinBy("-"),
    "DOT_SEPARATED": JoinBy("."),
    "SLASH_SEPARATED": JoinBy("/"),
    "DOUBLE_UNDERSCORE": JoinBy("__"),
    "DOUBLE_COLON_SEPARATED": JoinBy("::"),
    "NO_SPACES": JoinBy(""),
}

# This is the mapping from spoken phrases to formatters
mod.list("formatter_code", desc="List of code formatters")
mod.list(
    "formatter_code_extra",
    desc="List of extra code formatters, meant to be overwritten",
)
mod.list("formatter_prose", desc="List of prose formatters")
mod.list(
    "formatter_prose_extra",
    desc="List of extra prose formatters, meant to be overwritten",
)
mod.list("formatter_word", desc="List of word formatters")

FORMATTER_CODE = {
    "upper": "ALL_UPPERCASE",
    "lower": "ALL_LOWERCASE",
    "string": "DOUBLE_QUOTED_STRING",
    "quote": "SINGLE_QUOTED_STRING",
    "title": "CAPITALIZE_ALL",
    "camel": "NO_SPACES,CAPITALIZE_REST",
    "pascal": "NO_SPACES,CAPITALIZE_ALL",
    "snake": "SNAKE_CASE",
    "constant": "ALL_UPPERCASE,SNAKE_CASE",
    "kebab": "DASH_SEPARATED",
    "dotted": "DOT_SEPARATED",
    "slasher": "SLASH_SEPARATED",
    "dunder": "ALL_LOWERCASE,DOUBLE_UNDERSCORE",
    "packed": "DOUBLE_COLON_SEPARATED",
    "smash": "NO_SPACES",
    "trot": "TRAILING_PADDING",
}
ctx.lists["self.formatter_code"] = FORMATTER_CODE

FORMATTER_PROSE = {
    "say": "NOOP",
    "sentence": "CAPITALIZE_FIRST",
}
ctx.lists["self.formatter_prose"] = FORMATTER_PROSE

FORMATTER_WORD = {"word": "NOOP"}
ctx.lists["self.formatter_word"] = FORMATTER_WORD


@mod.capture(rule="({self.formatter_code} | {self.formatter_code_extra})+")
def formatters(m) -> str:
    """Return a comma-separated string of formatters, e.g., 'DOUBLE_QUOTED_STRING,CAPITALIZE_FIRST_WORD'."""
    return ",".join(m)


@mod.capture(rule="<user.formatters> [lit] <user.chunks>")
def formatted_code(m) -> str:
    """"""
    return Formatter.from_description(m.formatters)(m.chunks)


@mod.capture(rule="({self.formatter_prose} | {self.formatter_prose_extra})+")
def formatters_prose(m) -> str:
    """Return a comma-separated string of formatters, e.g., 'DOUBLE_QUOTED_STRING,CAPITALIZE_FIRST_WORD'."""
    return ",".join(m)


@mod.capture(rule="<user.formatters_prose> [lit] <user.prose>")
def formatted_prose(m) -> str:
    """"""
    return Formatter.from_description(m.formatters_prose)(m.prose.split())


@mod.capture(rule="({self.formatter_word})+")
def formatters_word(m) -> str:
    """Return a comma-separated string of formatters, e.g., 'DOUBLE_QUOTED_STRING,CAPITALIZE_FIRST_WORD'."""
    return ",".join(m)


@mod.capture(rule="<user.formatters_word> [lit] <user.word>")
def formatted_word(m) -> str:
    """"""
    return Formatter.from_description(m.formatters_word)((m.word,))


@mod.action_class
class Actions:
    def format_text(text: str, formatter_names: str) -> str:
        """
        Formats a text according to <formatter_names>.

        Args:
            formatter_names: A comma-separated string of formatters, e.g., 'CAPITALIZE_ALL_WORDS,DOUBLE_QUOTED_STRING'.
        """
        global FORMATTERS_DICT
        for formatter_name in reversed(formatter_names.split(",")):
            text = FORMATTERS_DICT[formatter_name](text)
        return text

    def unformat_text(text: str) -> str:
        """Remove format from text"""
        text = de_string(text)
        text = de_delim(text)
        text = de_camel(text)
        text = text.lower()
        return text


def de_camel(text: str) -> str:
    global REGEX_CAMEL_BOUNDARY
    return re.sub(REGEX_CAMEL_BOUNDARY, " ", text)


def de_delim(text: str) -> str:
    global REGEX_DELIMITER
    return re.sub(REGEX_DELIMITER, " ", text)


def de_string(text: str) -> str:
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    if text.startswith("'") and text.endswith("'"):
        return text[1:-1]
    return text


# Help menus


@imgui.open(x=ui.main_screen().x, y=ui.main_screen().y)
def gui(gui: imgui.GUI):
    global FORMATTER_CODE, FORMATTER_PROSE, FORMATTER_WORD
    gui.text("Formatters")
    gui.line()
    formatters = {**FORMATTER_CODE, **FORMATTER_PROSE, **FORMATTER_WORD}
    for name in frozenset(formatters):
        example = actions.user.format_text("one two three", formatters[name])
        gui.text(f"{name.ljust(30)}{example}")
    gui.spacer()
    if gui.button("Hide"):
        actions.user.help_hide_formatters()


mod = Module()
mod.mode(
    "help_formatters",
    desc="A mode which is active if the help GUI for formatters is showing",
)


@mod.action_class
class HelpActions:
    def help_show_formatters():
        """Show help GUI for formatters"""
        if not gui.showing:
            actions.mode.enable("user.help_formatters")
            gui.show()

    def help_hide_formatters():
        """Hide help GUI for formatters"""
        if gui.showing:
            actions.mode.disable("user.help_formatters")
            gui.hide()

    def help_toggle_formatters():
        """Toggle help GUI for formatters"""
        if gui.showing:
            actions.user.help_hide_formatters()
        else:
            actions.user.help_show_formatters()
