from talon import Context, Module, actions
from user.core import csv

mod = Module()

ctx = Context()
ctx.matches = r"""
tag: user.haskell
tag: user.auto_lang
and code.language: haskell
"""

# support for #user.code_library
csv.register(
    csv_file="code/haskell/libraries.csv",
    list_name="user.code_library",
    column_name="Library name",
    ctx=ctx,
)

# support for #user.code_operator
csv.register(
    csv_file="code/haskell/operators.csv",
    list_name="user.code_operator",
    column_name="Operator",
    ctx=ctx,
)

@mod.action_class
class UserActions:
    def haskell_qualified_letter(library: str) -> str:
        """Abbreviate module name using a single letter, e.g., Data.Map -> M."""
        return library.split(".")[-1][0]

    def haskell_qualified_word(library: str) -> str:
        """Abbreviate module name using a single word, e.g., Data.Map -> Map."""
        return library.split(".")[-1]

