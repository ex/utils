import sublime_plugin

try:  # Python 3
    from .haxe_generate_code_helper import *
except (ValueError):  # Python 2
    from haxe_generate_code_helper import *


class HaxeExtractVar(sublime_plugin.TextCommand):

    def find_insert_pos(self, src):
        ctx = self.context
        terminator_chars = ';{}'
        space_chars = ' \t'
        new_line_pos = -1
        sel_r = self.view.sel()[0]

        for i in range(
                sel_r.begin() - 1, ctx.method.block.begin() - 1, -1):
            c = src[i]

            if c == '\n':
                if new_line_pos == -1:
                    new_line_pos = i
            elif c in terminator_chars and new_line_pos != -1:
                break
            elif c not in space_chars:
                new_line_pos = -1

        if new_line_pos == -1:
            new_line_pos = ctx.method.block.begin() - 1

        pos = 0
        indent = ''
        for i in range(new_line_pos + 1, sel_r.begin()):
            c = src[i]
            if c not in space_chars:
                pos = i
                break
            indent += c

        return pos, indent

    def get_text(self, src, pos, indent):
        view = self.view
        unindent = '\n' + indent

        sel_r = view.sel()[0]
        sel = view.substr(sel_r)
        sel = '\n'.join(sel.split(unindent))

        pre_sel = view.substr(sublime.Region(pos, sel_r.begin()))
        pre_sel = '\n'.join(pre_sel.split(unindent))

        post_sel = ''
        pos_end = 0
        for i in range(sel_r.end(), view.size()):
            c = src[i]
            if c == '\n':
                pos_end = i
                break
            post_sel += c

        return \
            ('var ${1:name}${2::Dynamic} = %s;\n%s$1$0%s' %
                (sel, pre_sel, post_sel), pos_end)

    @staticmethod
    def poll(ctx):
        view = ctx.view
        cmds = []

        if not ctx.method or len(view.sel()) > 1 or view.sel()[0].empty():
            return cmds

        sel = view.sel()[0]

        if not ctx.method.block.contains(sel.begin()) or \
                not ctx.method.block.contains(sel.end()):
            return cmds

        cmds.append((
            'Extract Local Variable',
            'haxe_extract_var',
            {}))

        return cmds

    def run(self, edit):
        view = self.view

        if view is None or view.is_loading() or not is_haxe_scope(view):
            return

        self.context = get_context(view)

        if not self.context.method:
            return

        src = self.context.src
        pos, indent = self.find_insert_pos(src)
        text, pos_end = self.get_text(src, pos, indent)

        view.erase(edit, sublime.Region(pos, pos_end))
        set_pos(view, pos)
        view.run_command('insert_snippet', {"contents": text})
