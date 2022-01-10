tag: user.python_forced
tag: user.auto_lang
and code.language: python
-
tag(): user.code_data
tag(): user.code_exception
tag(): user.code_function
tag(): user.code_library
tag(): user.code_operator
tag(): user.code_type
settings():
    user.code_function_catch_all = "SNAKE_CASE"
    user.code_library_catch_all = "DOT_SEPARATED"
    user.code_type_catch_all = "PASCAL_CASE"

# support for #user.code_exception
raise {user.code_exception}:
    "raise {code_exception}"

except {user.code_exception}:
    "except {code_exception}:"

except {user.code_exception} as:
    "except {code_exception} as :"
    edit.left()

# support for #user.code_function
(deaf|define) funk <user.code_function_catch_all>:
    "def {code_function_catch_all}():"
    edit.insert_line_below()
    "pass"
    edit.up()
    edit.line_end()
    edit.left()
    edit.left()

# support for #user.code_library
import <user.code_library>$:
    "import {code_library}"

from <user.code_library> import everything$:
    "from {code_library} import {code_library_catch_all}\n"

from <user.code_library> import:
    "from {code_library} import "

# support for #user.code_type
has type <user.code_type>$:
    ": {code_type}"

returns type <user.code_type>:
    " -> {code_type}"