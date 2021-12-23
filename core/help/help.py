from talon import Module, Context, actions

mod = Module()
mod.list("help_menu", desc="")

help_menus = {
    "alphabet": (actions.user.help_show_alphabet, actions.user.help_hide_alphabet),
    "context": (actions.user.help_show_context, actions.user.help_hide_context),
    "formatters": (
        actions.user.help_show_formatters,
        actions.user.help_hide_formatters,
    ),
    "history": (actions.user.help_show_history, actions.user.help_hide_history),
    "scope": (actions.user.help_show_scope, actions.user.help_hide_scope),
    "search": (actions.user.help_show_search, actions.user.help_hide_search),
    "snippet": (actions.user.help_show_snippet, actions.user.help_hide_snippet),
}

ctx = Context()
ctx.lists["self.help_menu"] = {help_menu: help_menu for help_menu in help_menus.keys()}


@mod.action_class
class HelpActions:
    def help_show(text: str):
        """"""
        global help_menus
        if text in help_menus:
            show, hide = help_menus[text]
            show()

    def help_hide(text: str):
        """"""
        global help_menus
        if text in help_menus:
            show, hide = help_menus[text]
            hide()

    def help_hide_all():
        """"""
        global help_menus
        for show, hide in help_menus.values():
            hide()