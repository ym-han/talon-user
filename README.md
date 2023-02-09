This is my fork of Wen Kokke's talon user scripts.

# Organization

- `apps/` contains Talon scripts associated with applications, e.g., Safari;
- `core/` contains Talon scripts which are always running;
- `tags/` contains Talon scripts which are activated by a certain tag;
- `tags/code/` contains Talon scripts which are associated with a programming language, e.g., Haskell;
- `tags/code/tags/` contains Talon scripts which abstract over programming language features, e.g., comments.
- `util` contains Python scripts which may be imported

# TODO

- Extract lists to CSV files
  - `delimiters.py`: `delimiters_spaced`
  - `delimiters.py`: `delimiter_pair`
  - `keys.py`: `key_special`
  - `keys.py`: `key_modifier`
  - `keys.py`: `key_punctuation`
  - `keys.py`: `key_symbol`
  - `formatters.py`: `formatter_code`
  - `formatters.py`: `formatter_prose`
  - `formatters.py`: `formatter_word`
- Debug Talon HUD
