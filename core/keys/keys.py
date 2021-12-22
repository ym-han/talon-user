from talon import Module, Context, actions, app, imgui, registry, ui
from user.util import csv

mod = Module()
ctx = Context()
mod.tag("keys")

mod.list("key_alphabet", desc="The spoken phonetic alphabet")

KEY_ALPHABET = {}


def on_ready_and_change(letters: tuple[tuple[str]]):
    global ctx, KEY_ALPHABET
    KEY_ALPHABET = dict(letters)
    ctx.lists["self.key_alphabet"] = KEY_ALPHABET


csv.watch(
    csv_file="alphabet.csv",
    header=("Letter", "Spoken form"),
    on_success=on_ready_and_change,
)

DIGITS = "zero one two three four five six seven eight nine ten eleven twelve".split()
KEY_NUMBER = {DIGITS[i]: str(i) for i in range(10)}

mod.list("key_number", desc="All number keys")
ctx.lists["self.key_number"] = KEY_NUMBER

mod.list("key_function", desc="All function keys")
ctx.lists["self.key_function"] = {f"F {DIGITS[i]}": f"f{i}" for i in range(1, 13)}

mod.list("key_arrow", desc="All arrow keys")
ctx.lists["self.key_arrow"] = {"up", "down", "left", "right"}

mod.list("key_special", desc="All special keys")
ctx.lists["self.key_special"] = {
    "enter": "enter",
    "tab": "tab",
    "delete": "delete",
    "backspace": "backspace",
    "home": "home",
    "end": "end",
    "insert": "insert",
    "escape": "escape",
    "menu": "menu",
    "page up": "pageup",
    "page down": "pagedown",
    "print screen": "printscr",
}

mod.list("key_modifier", desc="All modifier keys")
ctx.lists["self.key_modifier"] = {
    "alt": "alt",
    "control": "ctrl",
    "shift": "shift",
    "super": "super",
}

# Symbols you want available BOTH in dictation and command mode.
mod.list("key_punctuation", desc="Symbols for inserting punctuation into text")
ctx.lists["self.key_punctuation"] = {
    "ampersand": "&",
    "back tick": "`",
    "comma": ",",
    "period": ".",
    "full stop": ".",
    "semicolon": ";",
    "colon": ":",
    "forward slash": "/",
    "question mark": "?",
    "exclamation mark": "!",
    "asterisk": "*",
    "hash sign": "#",
    "percent sign": "%",
}

# Symbols available in command mode, but NOT during dictation.
mod.list("key_symbol", desc="All symbols from the keyboard")
ctx.lists["self.key_symbol"] = {
    "dot": ".",
    "dash": "-",
    "prime": "'",
    "space": " ",
    "brick": "`",
    "slash": "/",
    "backslash": "\\",
    "minus": "-",
    "equal": "=",
    "plus": "+",
    "tilde": "~",
    "bang": "!",
    "down score": "_",
    "under score": "_",
    "question": "?",
    "snow": "*",
    "single": "'",
    "double": '"',
    "leper": "(",
    "repper": ")",
    "lack": "[",
    "rack": "]",
    "lace": "{",
    "race": "}",
    "langle": "<",
    "wrangle": ">",
    "pound": "#",
    "percy": "%",
    "tangle": "^",
    "amper": "&",
    "pipe": "|",
    "semi": ";",
    "stack": ":",
    "drip": ",",
    "at sign": "@",
    "hash": "#",
}


@mod.capture(rule="{self.key_modifier}+")
def key_modifiers(m) -> str:
    "One or more modifier keys"
    return "-".join(m.key_modifier_list)


@mod.capture(
    rule="( {self.key_alphabet} | {self.key_number} | {self.key_symbol} | {self.key_special} | {self.key_arrow} | {self.key_function} )"
)
def key_unmodified(m) -> str:
    "A single key with no modifiers"
    return str(m)


@mod.capture(rule="spell {self.key_alphabet}+")
def spell(m) -> str:
    """Spell word phoneticly"""
    return "".join(m.key_alphabet_list)


@mod.capture(rule="({self.key_alphabet} | {self.key_number} | {self.key_symbol})")
def any_alphanumeric_key(m) -> str:
    "any alphanumeric key"
    return str(m)


@mod.capture(rule="{self.key_alphabet}")
def letter(m) -> str:
    """One letter in the alphabet"""
    return str(m)


@mod.capture(rule="{self.key_alphabet}+")
def letters(m) -> str:
    """One or more letters in the alphabet"""
    return "".join(m.key_alphabet_list)


# Help menus


@imgui.open(x=ui.main_screen().x)
def gui(gui: imgui.GUI):
    global KEY_ALPHABET
    gui.text("Alphabet")
    gui.line()
    for spoken_form, letter in KEY_ALPHABET.items():
        gui.text(f"{letter}:  {spoken_form}")
    gui.spacer()
    if gui.button("Hide"):
        actions.user.help_hide("alphabet")


app.register("ready", lambda: actions.user.help_register("alphabet", gui))
