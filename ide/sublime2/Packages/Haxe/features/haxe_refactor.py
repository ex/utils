import glob
import os
import sublime
import sublime_plugin

try:  # Python 3
    from .haxe_helper import HaxeComplete_inst, runcmd
    from .haxe_generate_code_helper import is_haxe_scope
except (ValueError):  # Python 2
    from haxe_helper import HaxeComplete_inst, runcmd
    from haxe_generate_code_helper import is_haxe_scope


def join_pack(a, b):
    if a == '':
        return b
    return a + '.' + b


def to_disk_path_form(classpath, path, is_module=False):
    p = [classpath]
    p.extend(path.split('.'))
    if is_module:
        p[-1] = p[-1] + '.hx'
    return os.path.join(*p)


def to_haxe_form(classpath, path, is_module=False):
    relpath = os.path.relpath(path, classpath)
    if relpath == '.':
        relpath = ''
    elif is_module:
        relpath = relpath.rpartition('.')[0]
    relpath = relpath.replace(os.sep, '.')
    return relpath


class HaxeRefactor(sublime_plugin.WindowCommand):

    is_installed = -1

    @staticmethod
    def check_refactor_lib(view):
        settings = view.settings()
        haxelib_path = settings.get("haxelib_path", "haxelib")
        res, err = runcmd([haxelib_path, 'run', 'refactor'], '')

        HaxeRefactor.is_installed = 1
        if 'is not installed' in res:
            HaxeRefactor.is_installed = 0

    @staticmethod
    def poll(ctx):
        view = ctx.view
        cmds = []

        if HaxeRefactor.is_installed == -1:
            HaxeRefactor.check_refactor_lib(ctx.view)
        if HaxeRefactor.is_installed == 0:
            return cmds

        classpath = HaxeComplete_inst().get_build(view).get_classpath(view)
        if classpath is None or classpath not in view.file_name():
            return cmds

        for w in sublime.windows():
            for v in w.views():
                if v.is_dirty():
                    return cmds

        # if ctx.word:
        if True:
            cmds.append((
                'Rename/Move module ...',
                'haxe_refactor',
                {'mode': 'module'}))
        if True:
            cmds.append((
                'Rename package ...',
                'haxe_refactor',
                {'mode': 'package'}))

        return cmds

    def extract_modules(self, path, package=''):
        classes = []
        packs = []

        if not os.path.exists(path):
            return classes, packs

        for f in os.listdir(path):
            if os.path.isdir(os.path.join(path, f)):
                subpackage = join_pack(package, f)
                packs.append(subpackage)

                subclasses, subpacks = self.extract_modules(
                    os.path.join(path, f), subpackage)

                classes.extend(subclasses)
                packs.extend(subpacks)
            else:
                cname, ext = os.path.splitext(f)
                if ext == '.hx':
                    classes.append(join_pack(package, cname))

        if package == '':
            classes.sort()
            packs.sort()

        return classes, packs

    def on_input(self, input):
        view = self.window.active_view()
        settings = view.settings()
        haxelib_path = settings.get("haxelib_path", "haxelib")
        is_module = self.mode == 'module'
        files_to_open = []

        old = to_disk_path_form(self.classpath, self.option, is_module)
        new = to_disk_path_form(self.classpath, input, is_module)

        if self.mode == 'module':
            for w in sublime.windows():
                for v in w.views():
                    if v.file_name() == old:
                        w.focus_view(v)
                        w.run_command('close')
                        files_to_open.append(new)
        elif self.mode == 'package':
            for w in sublime.windows():
                for v in w.views():
                    if old in v.file_name():
                        relpath = os.path.relpath(v.file_name(), old)
                        files_to_open.append(os.path.join(new, relpath))
                        w.focus_view(v)
                        w.run_command('close')

        res, err = runcmd([
            haxelib_path, 'run', 'refactor', '-vv', 'rename',
            self.classpath, old, new], '')
        print('\nRefactor:\n' + res)

        for f in files_to_open:
            self.window.open_file(f)

    def on_select(self, index):
        if index == -1:
            return

        self.option = self.options[index]
        caption = ''
        if self.mode == 'module':
            caption = 'New module name for %s' % self.option
        elif self.mode == 'package':
            caption = 'New package name for %s' % self.option

        self.window.show_input_panel(
            caption, self.option, self.on_input, None, None)

    def run(self, mode=None):
        view = self.window.active_view()

        if view is None or view.is_loading() or not is_haxe_scope(view):
            return

        self.classpath = \
            HaxeComplete_inst().get_build(view).get_classpath(view)
        if self.classpath is None:
            return

        self.classes, self.packages = self.extract_modules(self.classpath)
        self.mode = mode

        idx = 0
        self.options = None
        if mode == 'module':
            self.options = self.classes
            cl = to_haxe_form(self.classpath, view.file_name(), True)
            if cl in self.options:
                idx = self.options.index(cl)
        elif mode == 'package':
            self.options = self.packages
            pk = to_haxe_form(
                self.classpath, os.path.dirname(view.file_name()))
            if pk in self.options:
                idx = self.options.index(pk)
        else:
            return

        self.window.show_quick_panel(self.options, self.on_select, 0, idx)
