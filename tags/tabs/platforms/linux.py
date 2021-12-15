from talon import Context, actions

# NOTE: some actions require easy window switcher

ctx = Context()
ctx.matches = r"""
os: linux
"""


@ctx.action_class("app")
class TabActions:
    @staticmethod
    def tab_close():
        actions.key("ctrl-w")

    @staticmethod
    def tab_next():
        actions.key("ctrl-tab")

    @staticmethod
    def tab_open():
        actions.key("ctrl-t")

    @staticmethod
    def tab_previous():
        actions.key("ctrl-shift-tab")

    @staticmethod
    def tab_reopen():
        actions.key("ctrl-shift-t")