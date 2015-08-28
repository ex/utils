import os
import re
import sublime
import sublime_plugin

try:  # Python 3
    from .haxe_helper import HaxeComplete_inst
    from .haxe_generate_code_helper import is_haxe_scope
except (ValueError):  # Python 2
    from haxe_helper import HaxeComplete_inst
    from haxe_generate_code_helper import is_haxe_scope

re_type = re.compile(r'(abstract|class|enum|interface|typedef)\s*\b([\w]*)\b')
re_package = re.compile(r'package\s*([\w.]*);')


def gen_package_decl(package):
    if package == '':
        return 'package;'
    return 'package %s;' % package


class HaxeFixModule(sublime_plugin.TextCommand):

    @staticmethod
    def poll(ctx):
        view = ctx.view
        cmds = []

        classpath = HaxeComplete_inst().get_build(view).get_classpath(view)
        if classpath is None:
            return cmds

        filename = os.path.splitext(os.path.basename(view.file_name()))[0]
        filedir = os.path.dirname(view.file_name())
        src = ctx.src

        mos = [mo for mo in re_type.finditer(src)]
        if len(mos) == 1:
            mo = mos[0]
            if filename != mo.group(2):
                cmds.append((
                    'Rename %s %s to %s' % (
                        mo.group(1), mo.group(2), filename),
                    'haxe_fix_module',
                    {'cname': filename}))

        mo = re_package.search(src)
        cur_package = mo.group(1) if mo else ''
        if classpath in filedir:
            package = os.path.relpath(filedir, classpath)
            if package == '.':
                package = ''
            package = package.replace(os.sep, '.')

            if package != cur_package:
                cmds.append((
                        'Rename package \'%s\' to \'%s\'' % (
                            cur_package, package),
                        'haxe_fix_module',
                        {'package': package}))

        return cmds

    def run(self, edit, cname=None, package=None):
        view = self.view

        if view is None or view.is_loading() or not is_haxe_scope(view):
            return

        src = view.substr(sublime.Region(0, self.view.size()))

        if cname is not None:
            mo = re_type.search(src)
            view.replace(edit, sublime.Region(mo.start(2), mo.end(2)), cname)
            sublime.status_message(
                '%s %s renamed to %s' % (mo.group(1), mo.group(2), cname))

        if package is not None:
            mo = re_package.search(src)
            if mo:
                view.replace(
                    edit, sublime.Region(mo.start(0), mo.end(0)),
                    gen_package_decl(package))
            else:
                view.insert(edit, 0, gen_package_decl(package) + '\n')
            sublime.status_message('package renamed')
