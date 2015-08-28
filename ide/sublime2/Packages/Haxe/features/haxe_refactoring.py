import sublime
import sublime_plugin

try:  # Python 3
    from .haxe_generate_code_helper import is_haxe_scope, get_context
    from .haxe_fix_module import HaxeFixModule
    from .haxe_refactor import HaxeRefactor
    from .haxe_promote_var import HaxePromoteVar
    from .haxe_usage import HaxeUsage
except (ValueError):  # Python 2
    from haxe_generate_code_helper import is_haxe_scope, get_context
    from haxe_fix_module import HaxeFixModule
    from haxe_refactor import HaxeRefactor
    from haxe_promote_var import HaxePromoteVar
    from haxe_usage import HaxeUsage


class HaxeRefactoring(sublime_plugin.WindowCommand):

    modules = [
        HaxeFixModule,
        HaxeUsage,
        HaxePromoteVar,
        HaxeRefactor
    ]

    def complete(self):
        cmd_name = self.cmd[1]
        args = self.cmd[2]

        self.window.run_command(cmd_name, args)

    def on_select(self, index):
        if index == -1:
            return

        self.cmd = self.cmds[index]
        self.cmds = None

        sublime.set_timeout(lambda: self.complete(), 10)

    def run(self):
        win = self.window
        view = win.active_view()

        if view is None or view.is_loading() or not is_haxe_scope(view):
            return

        self.context = get_context(view)

        self.cmds = []
        for gen in HaxeRefactoring.modules:
            self.cmds.extend(gen.poll(self.context))

        items = []
        for cmd in self.cmds:
            items.append(cmd[0])

        win.show_quick_panel(items, self.on_select)
