import sublime
import sublime_plugin
import re
from copy import deepcopy
from os.path import basename

try:  # Python 3
    from .haxe_helper import packageLine, show_quick_panel, \
        typeDecl, HaxeComplete_inst, comments
    from .haxe_generate_code_helper import count_blank_lines, get_blank_lines
except (ValueError):  # Python 2
    from haxe_helper import packageLine, show_quick_panel, \
        typeDecl, HaxeComplete_inst, comments
    from haxe_generate_code_helper import count_blank_lines, get_blank_lines


re_type = re.compile(r'\b(\w+\.)*[A-Z]\w*\b')
re_word = re.compile(r'\b[_a-zA-Z]\w*\b')
re_string = re.compile(r'(["\'])(?:\\\\|\\\1|.)*?\1', re.M | re.S)
re_conditions = re.compile(r'[ \t]*#(if|elseif|else|end)', re.M)
re_import_line = re.compile(
    '([ \t]*)import\s+'
    '('
    '((\\b[a-z]\w*\.)*)'
    '((\\b[A-Z]\w*\.?|\*)+)'
    '(\\b[_a-z]\w*|\*)?'
    ')\s*;', re.M)
re_using_line = re.compile(
    '^([ \t]*)using\s+'
    '('
    '((\\b[a-z]\w*\.)*)'
    '((\\b[A-Z]\w*\.?)+)'
    ')\s*;', re.M)


def add_type_path(type_map, typename, path):
    if typename in type_map:
        if is_string(type_map[typename]):
            if path != type_map[typename]:
                type_map[typename] = [type_map[typename], path]
        else:
            if path not in type_map[typename]:
                type_map[typename].append(path)
    else:
        type_map[typename] = path


def erase_line(view, edit, pos):
    rgn = view.full_line(pos)
    view.erase(edit, rgn)
    return rgn.end() - rgn.begin()


def get_cur_modulename(view):
    return basename(view.file_name()).partition('.')[0]


def get_cur_package(src):
    mo = packageLine.search(src)
    if mo is not None:
        return mo.group(1)
    return ''


def get_declared_typename_map(src):
    dct = {}

    for mo in typeDecl.finditer(src):
        dct[mo.group(2)] = True

    return dct


def get_full_imp(imppath, impname):
    if imppath == '':
        return impname
    if is_package(imppath) or not is_type(impname) or impname == '*':
        return '.'.join((imppath, impname))
    return imppath


def get_imported_clname_map(src, imp_to_ignore_map=None):
    dct = {}

    for mo in re_import_line.finditer(src):
        imp = mo.group(2)
        if imp_to_ignore_map is not None and imp in imp_to_ignore_map:
            continue
        impname = imp.rpartition('.')[2]
        dct[impname] = True

    return dct


def get_module_map(typenames):
    dct = {}

    for typename in typenames:
        if typename not in HaxeOrganizeImports.build_type_map:
            continue
        modules = HaxeOrganizeImports.build_type_map[typename]
        if not modules:
            continue
        if is_string(modules):
            if not is_package(modules):
                dct[modules] = True
        else:
            for module in modules:
                if not module:
                    continue
                if not is_package(module):
                    dct[module] = True

    return dct


def get_used_typename_map(src):
    dct = {}

    for mo in re_type.finditer(src):
        tp = mo.group(0)
        if '.' not in tp:
            if is_type(tp):
                dct[tp] = True
        else:
            words = tp.split('.')
            if not is_type(words[0]):
                continue
            for word in words:
                if is_type(word):
                    dct[word] = True

    # print('\nOI: Used typenames')
    # print('\n'.join([i for i in sorted(dct.keys())]))
    return dct


def get_used_words_map(src):
    dct = {}

    for mo in re_word.finditer(src):
        dct[mo.group(0)] = True

    # print('\nOI: Used words')
    # print('\n'.join([i for i in sorted(dct.keys())]))
    return dct


def get_view_src(view):
    return view.substr(sublime.Region(0, view.size()))


def init_build_class_map(view):
    HaxeOrganizeImports.std_type_map = init_type_map(
        HaxeComplete_inst().__class__.stdClasses)

    # print('OI: Std')
    # lst = HaxeComplete_inst().__class__.stdClasses
    # print("\n".join([k for k in sorted(lst)]))

    build = HaxeComplete_inst().get_build(view)
    HaxeOrganizeImports.build_classes, _ = build.get_types()

    # print('OI: Build')
    # lst = HaxeOrganizeImports.build_classes
    # print("\n".join([k for k in sorted(lst)]))

    HaxeOrganizeImports.build_type_map = init_type_map(
        HaxeOrganizeImports.build_classes,
        HaxeOrganizeImports.std_type_map)

    # print('OI: Map')
    # dct = HaxeOrganizeImports.build_type_map
    # print("\n".join([k + ': ' + str(dct[k]) for k in sorted(dct.keys())]))


def init_type_map(types, type_map=None):
    if type_map is None:
        type_map = {}
    else:
        type_map = deepcopy(type_map)

    for tp in types:
        tp, _, _ = tp.partition("<")
        path, _, typename = tp.rpartition(".")

        add_type_path(type_map, typename, path)

    return type_map


def is_haxe_scope(view):
    return view.score_selector(0, "source.haxe.2") > 0


def is_in_regions(regions, pos):
    for rgn in regions:
        if rgn.contains(pos):
            return True

    return False


def is_package(package):
    first_letter = package.rpartition('.')[2][0]
    return first_letter.lower() == first_letter


def is_string(value):
    val = False
    try:
        val = isinstance(value, basestring)
    except:
        val = isinstance(value, str)

    return val


def is_type(name):
    first_letter = name[0]
    return first_letter.upper() == first_letter


def search_conditional_regions(src):
    lines = []
    regions = []

    for mo in re_conditions.finditer(src):
        lines.append((mo.start(0), mo.group(1) == 'end'))

    last_pos = -1
    for pos, is_end in lines:
        if last_pos != -1:
            regions.append(sublime.Region(last_pos, pos))
        if is_end:
            last_pos = -1
        else:
            last_pos = pos

    return regions


class HaxeOrganizeImportsEdit(sublime_plugin.TextCommand):

    def insert_imports(self, edit):
        view = self.view
        imps = HaxeOrganizeImports.active_inst.imps_to_add

        pos = HaxeOrganizeImports.active_inst.insert_pos
        indent = HaxeOrganizeImports.active_inst.indent
        bl_group = get_blank_lines(view, 'haxe_bl_group', 1)
        ins = ''

        if pos > 0:
            if imps:
                ins += '\n'
            ins += bl_group

        for imp in imps:
            ins += '%simport %s;\n' % (indent, imp)

        if imps:
            ins = ins[:-1] + bl_group

        self.view.insert(edit, pos, ins)

    def remove_imports(self, edit):
        view = self.view

        for rgn in reversed(HaxeOrganizeImports.active_inst.rgns_to_remove):
            view.erase(edit, rgn)

        pos = HaxeOrganizeImports.active_inst.insert_pos
        _, after = count_blank_lines(view, pos)

        next_line_pos = view.full_line(pos).end()
        if after > 1:
            for i in range(0, after - 1):
                view.erase(edit, view.full_line(next_line_pos))

    def run(self, edit):
        if not HaxeOrganizeImports.active_inst:
            return

        self.remove_imports(edit)
        self.insert_imports(edit)

        HaxeOrganizeImports.active_inst.clean()


class HaxeOrganizeImports(sublime_plugin.WindowCommand):

    active_inst = None
    build_type_map = None
    build_classes = None
    std_type_map = None

    def add_unimported_classes(self):
        self.search_unimported_classes()

        if self.missing_impnames_to_prompt:
            self.prompt_classes_to_import()
        else:
            self.complete_adding_unimported_classes()

    def check_modules(self):
        module_map = get_module_map(self.used_typename_map.keys())
        imps_to_del = []

        for imp in self.imp_to_remove_map:
            if imp in module_map:
                imps_to_del.append(imp)

        for imp in imps_to_del:
            del self.imp_to_remove_map[imp]

    def clean(self):
        self.imps_to_add = None
        self.imp_to_remove_map = None
        self.rgns_to_remove = None
        self.missing_imps = None
        self.used_words_map = None
        self.used_typename_map = None
        self.imp_to_ignore_map = None
        HaxeOrganizeImports.active_inst = None

    def complete_adding_unimported_classes(self):
        if self.missing_imps:
            self.imps_to_add.extend(self.missing_imps)

        sublime.set_timeout(lambda: self.complete_command(), 10)

    def complete_command(self):
        removed_imports = []
        if self.imp_to_remove_map:
            for imp in self.imp_to_remove_map:
                if not self.remove or not self.imp_to_remove_map[imp]:
                    self.imps_to_add.append(imp)
                else:
                    removed_imports.append(imp)

        if self.sort:
            self.imps_to_add.sort()

        if ''.join(self.imports_before) == ''.join(self.imps_to_add):
            sublime.status_message('Allready organized')
            self.clean()
            return
        else:
            status = []
            n = len(self.missing_imps)
            if n == 1:
                status.append('Added %s' % self.missing_imps[0])
            elif n > 1:
                status.append('Added %d imports' % n)

            n = len(removed_imports)
            if n == 1:
                status.append('Removed %s' % removed_imports[0])
            elif n > 1:
                status.append('Removed %d imports' % n)

            sublime.status_message('; '.join(status))

        self.window.run_command('haxe_organize_imports_edit')

    def extract_imports(self):
        src = get_view_src(self.window.active_view())
        src = comments.sub('', src)
        src = re_string.sub('', src)

        self.src_wo_imports = src
        conditional_regions = search_conditional_regions(src)
        self.imp_to_remove_map = {}
        self.imp_to_ignore_map = {}
        self.imports_before = []
        self.indent = ''
        self.insert_pos = -1
        self.imps_to_add = []
        splitted_imps_to_add = []
        wildcard_path_map = {}
        cur_package = get_cur_package(src)
        self.rgns_to_remove = []
        offset = 0

        for mo in re_import_line.finditer(src):
            imp = mo.group(2)
            imppath, _, impname = imp.rpartition('.')
            self.imports_before.append(imp)

            self.src_wo_imports = \
                self.src_wo_imports[:mo.start(0) - offset] + \
                self.src_wo_imports[mo.end(0) - offset + 1:]
            offset += mo.end(0) - mo.start(0) + 1

            if is_in_regions(conditional_regions, mo.start(0)):
                self.imp_to_ignore_map[imp] = True
                continue

            if self.insert_pos == -1:
                self.insert_pos = mo.start(0)
                self.indent = mo.group(1)

            if imppath == '' or imppath == cur_package:
                self.imp_to_remove_map[imp] = True
            else:
                splitted_imps_to_add.append((imppath, impname))
            if impname == '*':
                wildcard_path_map[imppath] = True

            self.rgns_to_remove.append(sublime.Region(mo.start(0), mo.end(0)))

        while True:
            if not splitted_imps_to_add:
                break
            imppath, impname = splitted_imps_to_add.pop()
            if impname == '*' or imppath not in wildcard_path_map:
                self.imps_to_add.append(
                    get_full_imp(imppath, impname))

        offset = 0
        for mo in re_using_line.finditer(self.src_wo_imports):
            self.src_wo_imports = \
                self.src_wo_imports[:mo.start(0) - offset] + \
                self.src_wo_imports[mo.end(0) - offset + 1:]
            offset += mo.end(0) - mo.start(0) + 1

        self.used_words_map = get_used_words_map(self.src_wo_imports)
        self.used_typename_map = get_used_typename_map(self.src_wo_imports)

        self.insert_pos = self.get_insert_pos(src)

    def get_insert_pos(self, src):
        mo = packageLine.search(src)
        pos = 0
        if mo is not None:
            pos = mo.end(0)

        return pos

    @staticmethod
    def get_type_map(view):
        init_build_class_map(view)

        return HaxeOrganizeImports.build_type_map

    def on_select_class_to_import(self, index):
        if index == -1:
            self.clean()
            return

        impname = self.missing_impnames_to_prompt.pop()
        self.missing_imps.append(
            get_full_imp(
                HaxeOrganizeImports.build_type_map[impname][index],
                impname))

        if not self.missing_impnames_to_prompt:
            self.complete_adding_unimported_classes()
        else:
            self.prompt_classes_to_import()

    def on_select_import_to_remove(self, index):
        if index == -1:
            self.clean()
            return

        if index == 0:
            if self.add:
                sublime.set_timeout(lambda: self.add_unimported_classes(), 10)
            else:
                sublime.set_timeout(lambda: self.complete_command(), 10)
            return
        elif index < 3:
            for imp in self.imp_to_remove_map:
                self.imp_to_remove_map[imp] = \
                    True if index == 1 else False
        else:
            imp = sorted(self.imp_to_remove_map.keys())[index - 3]
            self.imp_to_remove_map[imp] = \
                not self.imp_to_remove_map[imp]

        self.prompt_imports_to_remove(index)

    def prompt_classes_to_import(self):
        impname = self.missing_impnames_to_prompt[-1]
        options = []

        for package in HaxeOrganizeImports.build_type_map[impname]:
            if package == '':
                self.missing_impnames_to_prompt.pop()
                if not self.missing_impnames_to_prompt:
                    self.complete_adding_unimported_classes()
                else:
                    self.prompt_classes_to_import()
                return
            options.append('import %s' % get_full_imp(package, impname))

        show_quick_panel(
            self.window, options, self.on_select_class_to_import,
            sublime.MONOSPACE_FONT, 0)

    def prompt_imports_to_remove(self, selected_index=0):
        if not self.imp_to_remove_map:
            if self.add:
                self.add_unimported_classes()
            else:
                self.complete_command()
            return

        options = []
        options.append('Done')
        options.append('Check All')
        options.append('Uncheck All')

        sorted_imps = sorted(self.imp_to_remove_map.keys())
        for imp in sorted_imps:
            options.append(
                '[%s] remove %s' %
                ('x' if self.imp_to_remove_map[imp] else ' ', imp))

        show_quick_panel(
            self.window, options, self.on_select_import_to_remove,
            sublime.MONOSPACE_FONT, selected_index)

    def remove_unused_imports(self):
        used_imps = []

        for imp in self.imps_to_add:
            if imp in used_imps:
                continue

            impname = imp.rpartition('.')[2]
            if impname != '*':
                if impname not in self.used_words_map:
                    self.imp_to_remove_map[imp] = True
                    continue

            used_imps.append(imp)

        self.imps_to_add = used_imps

    def run(self, add=True, sort=True, remove=True, auto_remove=True):
        view = self.window.active_view()
        if view is None or not is_haxe_scope(view):
            return

        HaxeOrganizeImports.active_inst = self
        self.add = add
        self.sort = sort
        self.remove = remove

        init_build_class_map(self.window.active_view())

        self.extract_imports()
        self.remove_unused_imports()
        self.check_modules()

        if remove and not auto_remove:
            self.prompt_imports_to_remove()
        elif add:
            self.add_unimported_classes()
        else:
            self.complete_command()

    def search_unimported_classes(self):
        self.missing_imps = []
        self.missing_impnames_to_prompt = []
        if HaxeOrganizeImports.build_type_map is None:
            return

        src = get_view_src(self.window.active_view())
        unimported_typename_map = {}
        unimported_typenames_to_prompt_map = {}
        imported_clname_map = \
            get_imported_clname_map(src, self.imp_to_ignore_map)
        declared_typename_map = get_declared_typename_map(src)
        cur_package = get_cur_package(src)

        for typename in self.used_typename_map:
            if typename not in HaxeOrganizeImports.build_type_map or \
                    typename in imported_clname_map or \
                    typename in declared_typename_map:
                continue

            if is_string(HaxeOrganizeImports.build_type_map[typename]):
                package = HaxeOrganizeImports.build_type_map[typename]

                if cur_package == package or package == '':
                    continue

                unimported_typename_map[typename] = True
            else:
                unimported_typenames_to_prompt_map[typename] = True

        for typename in unimported_typename_map.keys():
            self.missing_imps.append(
                get_full_imp(
                    HaxeOrganizeImports.build_type_map[typename], typename))

        # print('\nOI: Missing imports')
        # print('\n'.join(self.missing_imps))
        self.missing_impnames_to_prompt = \
            list(unimported_typenames_to_prompt_map.keys())
