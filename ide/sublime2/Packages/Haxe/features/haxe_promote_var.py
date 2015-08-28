import re
import sublime_plugin

try:  # Python 3
    from .haxe_generate_code_helper import *
    from .haxe_helper import HaxeComplete_inst
    from .haxe_format import format_statement
except (ValueError):  # Python 2
    from haxe_generate_code_helper import *
    from haxe_helper import HaxeComplete_inst
    from haxe_format import format_statement

re_s = re.compile(r'\s*$')


def get_type(view, pos, name):
    win = view.window()

    win.run_command(
        'haxe_promote_var_edit',
        {'pos0': pos, 'pos1': pos, 'text': '%s.|' % name})

    complete = HaxeComplete_inst()
    temp = complete.save_temp_file(view)
    tp = complete.run_haxe(view, dict(
        mode="type",
        filename=view.file_name(),
        offset=0,
        commas=None
    ))
    complete.clear_temp_file(view, temp)

    win.run_command('undo')

    return tp


class HaxePromoteVarEdit(sublime_plugin.TextCommand):

    def run(self, edit, pos0, pos1, text):
        pos0 = int(pos0)
        pos1 = int(pos1)
        self.view.replace(edit, sublime.Region(pos0, pos1), text)


class HaxePromoteVar(sublime_plugin.WindowCommand):

    def on_select(self, index):
        if index == -1:
            return

        view = self.window.active_view()
        txt = None
        if self.tp is not None:
            is_static = index != 0
            self.tp = format_statement(view, self.tp)
            txt = get_editable_mods(
                    view, 1, self.name[0] == '_',
                    0, 1, 0, is_static, 0, 1) + \
                'var %s$HX_W_C:${HX_C_W}%s;$0' % (self.name, self.tp)

        self.window.run_command('haxe_promote_var_edit', {
            'pos0': self.pos0,
            'pos1': self.pos1,
            'text': self.name + self.post
        })
        self.window.run_command('haxe_generate_field', {
            'name': self.name,
            'field': FIELD_VAR if index == 0 else FIELD_STATIC_VAR,
            'text': txt,
            'move': True
        })

    @staticmethod
    def poll(ctx):
        view = ctx.view
        cmds = []

        if not ctx.method or not ctx.word:
            return cmds

        src = view.substr(ctx.method.region)
        if re.search(r'var\s+' + ctx.word.name, src):
            cmds.append((
                'Promote Local Variable ...',
                'haxe_promote_var',
                {}))

        return cmds

    def run(self):
        win = self.window
        view = win.active_view()

        if view is None or view.is_loading() or not is_haxe_scope(view):
            return

        self.context = get_context(view)
        self.tp = None

        if not self.context.method or not self.context.word:
            return

        re_var = re.compile(
            r'(var\s+)' + self.context.word.name +
            r'(\s*:([a-zA-Z][\w\s.,<>]*))?' +
            r'([^;]*);', re.M)
        src = view.substr(self.context.method.region)
        last_mo = None
        method_pos = self.context.method.region.begin()
        word_pos = self.context.word.region.begin()

        for mo in re_var.finditer(src):
            if mo.start(0) + method_pos > word_pos:
                break
            last_mo = mo

        if last_mo:
            if last_mo.group(3):
                self.tp = last_mo.group(3).strip()
                self.post = (
                    re_s.search(last_mo.group(3)).group(0))
            else:
                self.tp = get_type(
                    view, last_mo.end(0) + method_pos, self.context.word.name)
                if self.tp is not None:
                    self.tp = shorten_imported_type(
                        self.tp, self.context.imports)
                self.post = (
                    re_s.search(last_mo.group(4)).group(0))

            self.pos0 = last_mo.start(1) + method_pos
            self.pos1 = last_mo.start(4) + method_pos
            self.name = self.context.word.name

            options = [
                'Promote var %s' % self.name,
                'Promote static var %s' % self.name]
            win.show_quick_panel(
                options, self.on_select, sublime.MONOSPACE_FONT, 0)
