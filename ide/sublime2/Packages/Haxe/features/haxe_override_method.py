import re
import sublime
import sublime_plugin

try:  # Python 3
    from .haxe_generate_code_helper import *
    from .haxe_format import format_statement
    from .haxe_helper import HaxeComplete_inst, show_quick_panel
except (ValueError):  # Python 2
    from haxe_generate_code_helper import *
    from haxe_format import format_statement
    from haxe_helper import HaxeComplete_inst, show_quick_panel

re_extends = re.compile(r'extends\s+([\w\.]+)', re.MULTILINE)
re_type_path = re.compile(r'\b(\w+\.)*([A-Z]\w*)\b')


class HaxeOverrideMethodEdit(sublime_plugin.TextCommand):

    def run(self, edit, pos, name):
        view = self.view
        tmp = 'function %s(){this.|}' % name
        pos = int(pos)

        view.insert(edit, pos, tmp)


class HaxeOverrideMethod(sublime_plugin.WindowCommand):

    def on_select(self, index):
        if index == -1:
            return

        view = self.window.active_view()
        field = self.methods[index]

        ftype = FIELD_FUNC
        fname = field[0]
        fparams = ','.join(field[1])
        fparams = format_statement(view, fparams)
        fparams = re_type_path.sub(r'\2', fparams)
        fargs = ','.join([s.partition(':')[0].strip() for s in field[1]])
        fargs = format_statement(view, fargs)
        ret = format_statement(view, field[2])
        ret = re_type_path.sub(r'\2', ret)

        ftext = \
            get_editable_mods(view, 1, 0, 1, 1, 0, 0, 0, 1) +\
            'function ' +\
            '%s$HX_W_ORB(${HX_ORB_W}%s$HX_W_CRB)$HX_CRB_W_C:${HX_C_W}%s' +\
            '$HX_W_OCB{\n\t' +\
            ('' if ret == 'Void' else '${2:return }') +\
            '${3:super.%s(${HX_ORB_W}%s$HX_W_CRB);}$0' +\
            '\n}'
        ftext = ftext % (fname, fparams, ret, fname, fargs)

        self.window.run_command(
            'haxe_generate_field',
            {'name': fname, 'field': ftype, 'text': ftext, 'move': True})

    @staticmethod
    def poll(ctx):
        if not ctx.type or ctx.type.group != 'class':
            return []

        src = ctx.view.substr(ctx.type.region)
        if re_extends.search(src) is None:
            return []

        return [(
            'Override Method...',
            'haxe_override_method',
            {})]

    def run(self):
        win = self.window
        view = win.active_view()

        if view is None or view.is_loading() or not is_haxe_scope(view):
            return

        self.context = get_context(view)

        if not self.context.type:
            return

        method_names = {'new': True}
        for methodCtx in self.context.type.methods:
            method_names[methodCtx.name] = True
        tmp_name = '__sublime_tmp_method__'
        method_names[tmp_name] = True

        win.run_command(
            'haxe_override_method_edit',
            {'pos': self.context.type.block.begin(), 'name': tmp_name})

        complete = HaxeComplete_inst()
        temp = complete.save_temp_file(view)
        _, _, _, _, fields = complete.run_haxe(view, dict(
            mode=None,
            filename=view.file_name(),
            offset=0,
            commas=None))
        complete.clear_temp_file(view, temp)

        win.run_command('undo')

        self.methods = []
        for field in fields:
            name = field[0]
            args = field[1]
            if args is None or name in method_names:
                continue
            self.methods.append(field)

        options = []
        for method in self.methods:
            options.append('%s()' % method[0])

        show_quick_panel(
            win, options, self.on_select, sublime.MONOSPACE_FONT, 0)
