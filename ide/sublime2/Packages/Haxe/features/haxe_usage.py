import codecs
import fnmatch
import os
import sublime
import sublime_plugin
import time
import re

try:  # Python 3
    from .haxe_helper import HaxeComplete_inst, get_classpaths
    from .haxe_generate_code_helper import is_haxe_scope, get_context
    from .haxe_organize_imports import HaxeOrganizeImports
    from .haxe_parse_helper import *
except (ValueError):  # Python 2
    from haxe_helper import HaxeComplete_inst, get_classpaths
    from haxe_generate_code_helper import is_haxe_scope, get_context
    from haxe_organize_imports import HaxeOrganizeImports
    from haxe_parse_helper import *

from xml.etree import ElementTree

try:
    from elementtree import SimpleXMLTreeBuilder
    ElementTree.XMLTreeBuilder = SimpleXMLTreeBuilder.TreeBuilder
except ImportError as e:
    pass  # ST3

result_file_regex = (
    r'^(.+):(\d+)'
    r'(?:: (?:lines \d+-\d+|character(?:s \d+-| )(\d+)) : )?'
    r'(?:(?!Defined in this class).)*$')
re_haxe_position = re.compile(
    r'^(.+):(\d+): (?:lines \d+-\d+|character(?:s (\d+)-| )(\d+))$')


def get_root_dir(filepath, package):
    n = 0
    if package:
        n = len(package.split('.'))
    else:
        return os.path.dirname(filepath)

    return os.path.realpath(os.path.abspath(os.path.join(
        os.path.dirname(filepath),
        os.sep.join([os.pardir] * n))))


class HaxeUsage(sublime_plugin.WindowCommand):

    is_active = False

    def append_usage(self, path, line):
        if self.root_dir not in path:
            return

        if path.find(self.result_base_dir) == 0:
            path = path[len(self.result_base_dir):].strip(os.sep)

        usage = '%s:%d' % (path, line)

        if usage not in self.usages:
            self.usages.append(usage)
            self.log(usage)

    def find_field_usages(self, filepath, line):
        # print('HU field:', filepath, line)
        field = self.context.word.name

        type_path, is_method, is_static, is_override = self.search_type(
            filepath, line)

        if is_method and not is_static:
            self.find_method_usages(type_path, is_override)
        else:
            self.find_usages(0, (type_path,), field, is_static)

    def find_inh_types(self, type_name, back=True):
        inh_type_map = {}
        inh_type_map[type_name] = True

        if back:
            while type_name in self.ext_map:
                type_name = self.ext_map[type_name]
                inh_type_map[type_name] = True

        for type_name in self.ext_map.keys():
            lst = []
            add = False
            while type_name in self.ext_map:
                lst.append(type_name)
                type_name = self.ext_map[type_name]
                if type_name in inh_type_map:
                    add = True
                    break

            if add:
                for i in lst:
                    inh_type_map[i] = True

        return [
            k for k in inh_type_map.keys()
            if k in self.contains_word_ext_map]

    def find_local_or_field_usages(self):
        self.show_panel()
        self.log('Find usages: %s' % self.word.name)

        # print('HU local_or_field')
        ctx = self.context

        is_param = ctx.method and \
            ctx.method.region.begin() < ctx.word.region.begin() and \
            self.word.region.end() <= ctx.method.block.begin() and \
            '(' in ctx.src[ctx.method.region.begin():ctx.word.region.begin()]

        complete = HaxeComplete_inst()
        temp = complete.save_temp_file(self.view, is_param)

        filepath = None
        usage_line = 0

        src = self.view.substr(
            sublime.Region(0, ctx.word.region.end()))
        offset = len(codecs.encode(src, 'utf-8')) + 1

        mos = [mo for mo in re.finditer(
            r'\b(for\s*\(\s*|var\s+|function\s+)%s\b' % ctx.word.name,
            src, re.M)]
        mo = mos[-1] if mos else None
        is_declaration = mo and mo.end(0) == ctx.word.region.end()
        is_field = False
        view_filepath = os.path.realpath(self.view.file_name())

        if is_declaration or is_param:
            filepath = os.path.realpath(self.view.file_name())
            usage_line, _ = self.view.rowcol(ctx.word.region.end())
            usage_line += 1
            self.append_usage(filepath, usage_line)

            if is_declaration:
                is_field = not ctx.method or \
                    ctx.word.region.end() <= ctx.method.block.begin()
        else:
            position = complete.run_haxe(self.view, dict(
                mode='position',
                filename=self.view.file_name(),
                offset=offset,
                commas=None
            ))

            if position:
                filepath, usage_line, begin, end = \
                    self.parse_and_append_usage(position)
                begin = self.view.text_point(usage_line, begin)
                end = self.view.text_point(usage_line, end)
                is_field = view_filepath != filepath or \
                    not ctx.method or \
                    end <= ctx.method.block.begin() or \
                    begin >= ctx.method.block.end()
            else:
                self.has_pos_errors = True

        if filepath:
            if filepath != view_filepath:
                self.find_field_usages(filepath, usage_line)
            else:
                if is_param:
                    self.find_param_usages(filepath)
                elif not is_field:
                    # print('HU local usages')
                    self.hx_files = [filepath]

                    if is_declaration:
                        self.find_local_usages(filepath, usage_line)
                    else:
                        self.find_usages(offset)
                else:
                    self.find_field_usages(filepath, usage_line)
        else:
            self.finish()

        complete.clear_temp_file(self.view, temp)

    def find_local_usages(self, filepath, usage_line):
        self.append_usage(self.view.file_name(), usage_line)

        rgn = self.word.region
        pos_cols = (
            self.view.rowcol(rgn.begin())[1],
            self.view.rowcol(rgn.end())[1])

        src = self.view.substr(sublime.Region(
            self.context.word.region.end(), self.context.method.region.end()))

        idx = 0
        idx = src.find(self.context.word.name, idx)
        complete = HaxeComplete_inst()

        while idx != -1:
            offset = self.context.word.region.end() + idx + \
                len(self.context.word.name)
            src_o = self.view.substr(sublime.Region(0, offset))
            offset = len(codecs.encode(src_o, 'utf-8')) + 1

            position = complete.run_haxe(self.view, dict(
                mode='position',
                filename=filepath,
                offset=offset,
                commas=None
            ))

            if position:
                mo = re_haxe_position.search(position)
                if mo:
                    line = int(mo.group(2))
                    cols = (int(mo.group(3)), int(mo.group(4)))

                    if line == usage_line and \
                            cols[0] <= pos_cols[0] and pos_cols[1] <= cols[1]:
                        self.find_usages(offset)
                        return
            else:
                self.has_pos_errors = True

            idx = src.find(self.context.word.name, idx + 1)

        self.finish()

    def find_method_positions(self, type_paths, word):
        # print('HU positions:', word)

        filepath = os.path.join(self.root_dir, 'SublimeHaxeUsage.hx')
        complete = HaxeComplete_inst()

        def find(idx, t):
            if idx >= len(type_paths):
                try:
                    os.remove(filepath)
                except OSError:
                    pass

                self.find_usages(0, type_paths, self.context.word.name)
                return

            t0 = time.time()

            type_path = type_paths[idx]
            s = (
                'class SublimeHaxeUsage {'
                'static var temp:%s;'
                'static function main() {temp.%s.|;}'
                '}'
                ) % (type_path, word)

            sublime.status_message('Find method in \'%s\'' % type_path)

            with open(filepath, 'w') as f:
                f.write(s)

            position = complete.run_haxe(self.view, dict(
                mode='position',
                filename=filepath,
                offset=0,
                commas=None
            ))

            if position:
                self.parse_and_append_usage(position)
            else:
                self.has_pos_errors = True

            t += time.time() - t0
            idx += 1

            if t > 0.5:
                t = 0
                sublime.set_timeout(lambda: find(idx, t), 10)
            else:
                find(idx, t)

        sublime.set_timeout(lambda: find(0, 0), 10)

    def find_method_usages(self, type_name, is_override):
        self.scan_hx_files(True)

        # print('HU method usages:', type_name)
        self.classpaths = get_classpaths(self.view)

        type_paths = self.find_inh_types(type_name, is_override)
        # print('HU type paths:', type_paths)

        self.find_method_positions(type_paths, self.context.word.name)

    def find_param_usages(self, filepath):
        # print('HU param usage')
        src = self.context.src
        src = src[:self.context.method.block.begin()] + \
            '%s' % self.context.word.name

        offset = len(codecs.encode(src, 'utf-8')) + 1

        src += ';' + self.context.src[self.context.method.block.begin():]
        complete = HaxeComplete_inst()

        with open(filepath, 'w') as f:
            f.write(src)

        usage = complete.run_haxe(self.view, dict(
            mode='usage',
            filename=filepath,
            offset=offset,
            commas=None
        ))

        if usage:
            tree = self.parse_xml(usage[0])

            if tree is not None:
                usages = [i.text for i in tree.getiterator('pos')]
                if usages:
                    usages.pop(0)
                for u in usages:
                    self.parse_and_append_usage(u)

        self.finish()

    def find_type_usages(self):
        type_name = self.context.word.name
        # print('HU type name:', type_name)

        type_path = None
        if self.context.src[self.word.region.begin() - 1] == '.':
            src = self.context.src[:self.word.region.end()]
            type_paths = re.findall(r'(?:\w+\.)+%s\b' % type_name, src)
            if type_paths:
                type_path = type_paths[-1]

        if not type_path:
            type_path = find_type_path(
                type_name, self.type_map,
                parse_imports(self.src_wo_comments, True),
                parse_package(self.src_wo_comments))
        # print('HU type path:', type_path)

        if not type_path:
            return

        self.show_panel()
        self.log('Find usages: %s' % type_path)

        type_package = get_package(type_path)
        # print('HU type package:', type_package)

        has_namesakes = not is_string(self.type_map[type_name])

        p, _, n = type_path.rpartition('.')
        re_type_usage = re.compile(r'\b(?:%s\.)?(%s)\b' % (p, n))
        re_type_path_usage = None
        re_type_path_or_name_usage = None

        namesakes = None if not has_namesakes else [
            join_type(p, type_name)
            for p in self.type_map[type_name]
            if (p != type_path.rpartition('.')[0] or not p and
                type_path.rpartition('.')[0] != '')
        ]
        # print('HU namesakes', namesakes)

        if p:
            re_type_path_usage = re.compile(r'\b%s\.(%s)\b' % (p, n))
            re_type_path_or_name_usage = re.compile(
                r'(?:%s\.|[^\.])\b(%s)\b' % (p, n))
        else:
            re_type_path_usage = \
                re_type_path_or_name_usage = re.compile(r'\b(%s)\b' % n)

        for root, dirnames, filenames in os.walk(self.root_dir):
            for filename in fnmatch.filter(filenames, '*.hx'):
                module_filepath = os.path.join(root, filename)

                with open(module_filepath) as f:
                    src = f.read()

                    comment_regions = find_comment_regions(src)
                    comment = 0
                    num_comments = len(comment_regions)

                    line_positions = find_line_positions(src)
                    line = 0
                    num_lines = len(line_positions)

                    re_obj = re_type_usage

                    if has_namesakes:
                        src_wo_comments = remove_comments(src)
                        imp_map = parse_imports(src_wo_comments, True)
                        type_name_map = parse_declared_type_names(
                            src_wo_comments, True)
                        package = parse_package(src_wo_comments)
                        re_obj = re_type_path_usage

                        if type_name in type_name_map:
                            if type_package == '':
                                if is_imported(
                                        namesakes,
                                        self.type_map, imp_map, False) or \
                                        package and \
                                        package in self.type_map[type_name]:
                                    re_obj = None
                            elif package == type_package:
                                re_obj = re_type_path_or_name_usage
                        else:
                            if type_package == '':
                                if is_imported(
                                        namesakes,
                                        self.type_map, imp_map, False) or \
                                        package and \
                                        package in self.type_map[type_name]:
                                    re_obj = None
                            elif is_imported(
                                    (type_path,), self.type_map, imp_map):
                                re_obj = re_type_path_or_name_usage
                            elif not is_imported(
                                    namesakes, self.type_map, imp_map,
                                    False) and \
                                    package == type_package:
                                re_obj = re_type_path_or_name_usage

                    if re_obj is None:
                        continue

                    for mo in re_obj.finditer(src):
                        while comment < num_comments and \
                                mo.end(0) > comment_regions[comment][1]:
                            comment += 1

                        if comment < num_comments and \
                                mo.start(0) >= comment_regions[comment][0]:
                            continue

                        while line < num_lines and \
                                line_positions[line] < mo.start(1):
                            line += 1
                        self.append_usage(module_filepath, line + 1)

        self.finish()

    def find_usages(
            self, offset=0, type_paths=None, field=None, is_static=False):
        static = 'true' if is_static else 'false'

        if self.hx_files is None:
            self.scan_hx_files()

        complete = HaxeComplete_inst()

        args = None
        if type_paths:
            field = 'null' if field is None else '"%s"' % field
            args = []
            for tp in type_paths:
                args.append((
                    '--macro',
                    'addMetadata("@:usage", "%s", %s, %s)' % (
                        tp, field, static)))

        num_files = len(self.hx_files)

        def find(idx, t):
            if idx >= num_files:
                self.finish()
                return

            t0 = time.time()

            f = self.hx_files[idx]
            sublime.status_message('Find usages in \'%s\'' % f)

            usage = complete.run_haxe(self.view, dict(
                mode='usage',
                filename=f,
                offset=offset,
                commas=None,
                serverMode=False),
                args)

            tree = self.parse_xml(usage[0])

            if tree is not None:
                for i in tree.getiterator('pos'):
                    self.parse_and_append_usage(i.text)

            t += time.time() - t0
            idx += 1

            if t > 0.5:
                t = 0
                sublime.set_timeout(lambda: find(idx, t), 10)
            else:
                find(idx, t)

        sublime.set_timeout(lambda: find(0, 0), 10)

    def finish(self):
        if self.usages:
            self.output_view.find_all_results()

        self.has_errors = self.has_errors or self.has_pos_errors
        if self.has_pos_errors:
            usage = HaxeComplete_inst().run_haxe(self.view, dict(
                mode='usage',
                filename=self.view.file_name(),
                offset=0,
                commas=None
            ))
            if usage:
                self.parse_xml(usage[0])
        self.log('[Finished]')

        HaxeUsage.is_active = False

    def log(self, text):
        self.output_view.run_command(
            'append',
            {
                'characters': text + '\n',
                'force': True,
                'scroll_to_end': True
            })

    def parse_and_append_usage(self, text):
        mo = re_haxe_position.search(text)
        if not mo:
            return (None, None)

        begin = -1
        end = -1

        if mo.group(3):
            begin = int(mo.group(3))
        if mo.group(4):
            end = int(mo.group(4))

        usage = (mo.group(1), int(mo.group(2)), begin, end)
        self.append_usage(usage[0], usage[1])

        return usage

    def parse_xml(self, text):
        try:
            tree = ElementTree.XML(text)
        except Exception as e:
            self.has_errors = True
            for line in [
                    l for l in text.split('\n')
                    if l and 'Defined in this class' not in l]:
                self.log(line)
            # print('HU error:', text)
            # print('HU error:', e)
            return None

        return tree

    @staticmethod
    def poll(ctx):
        if HaxeComplete_inst().compilerVersion < 3.2:
            return []

        for w in sublime.windows():
            for v in w.views():
                if v.is_dirty() and v.score_selector(0, 'source.haxe.2') > 0:
                    return []

        if ctx.word:
            return [(
                'Find Usages: %s ...' % ctx.word.name,
                'haxe_usage',
                {})]

        return []

    def run(self):
        if HaxeUsage.is_active:
            return

        win = self.window
        view = win.active_view()
        self.has_errors = False
        self.has_pos_errors = False
        self.view = view
        self.hx_files = None
        self.is_cancelled = False

        if view is None or view.is_loading() or not is_haxe_scope(view):
            return

        self.context = get_context(view)
        word = self.context.word
        self.word = word

        if not word:
            return

        HaxeUsage.is_active = True
        self.type_map = HaxeOrganizeImports.get_type_map(self.view)
        self.usages = []
        self.src_wo_comments = remove_comments(self.context.src)
        self.package = parse_package(self.src_wo_comments)

        # print('HU: ---------------------------------------')
        # print('HU:', word.name)

        self.root_dir = get_root_dir(
            self.view.file_name(), self.package)
        self.result_base_dir = os.path.abspath(
            os.path.join(self.root_dir, os.pardir))
        # print('HU root:', self.root_dir)

        if is_type(word.name, self.type_map):
            self.find_type_usages()
        else:
            self.find_local_or_field_usages()

    def scan_hx_files(self, gen_ext_map=False):
        self.hx_files = []
        if gen_ext_map:
            self.ext_map = {}
            self.contains_word_ext_map = {}
        word = self.context.word.name
        re_word = re.compile(r'\b%s\b' % word)

        for root, dirnames, filenames in os.walk(self.root_dir):
            for filename in fnmatch.filter(filenames, '*.hx'):
                if filename == 'SublimeHaxeUsage.hx':
                    continue

                filepath = os.path.join(root, filename)

                with open(filepath) as f:
                    src = remove_comments(f.read())

                    contains_word = re_word.search(src)
                    if contains_word:
                        self.hx_files.append(filepath)

                    if gen_ext_map:
                        mos = find_class_declarations(src)
                        imp_map = parse_imports(src, True)
                        package = parse_package(src)
                        for mo in mos:
                            type_path = None
                            if mo.group(1) is not None:
                                type_path = find_type_path(
                                    mo.group(1), self.type_map, imp_map,
                                    package)
                                if contains_word:
                                    self.contains_word_ext_map[type_path] = \
                                        True
                            if mo.group(2) is not None:
                                ext_type_path = find_type_path(
                                    mo.group(2), self.type_map, imp_map,
                                    package)
                                self.ext_map[type_path] = ext_type_path

        # print('HU files:', self.hx_files)

    def search_type(self, filepath, line):
        src = ''
        with open(filepath) as f:
            for ln in f:
                src += ln
                line -= 1
                if line <= 0:
                    break

        src = remove_comments(src)
        package = parse_package(src)
        type_name = ''

        mos = find_class_declarations(src)
        for mo in mos:
            type_name = mo.group(1)

        field_decl = find_field_declaration(src, self.context.word.name)
        field_decl_words = [] if not field_decl else field_decl.split(' ')

        is_static = 'static' in field_decl_words
        is_override = 'override' in field_decl_words
        is_method = 'function' in field_decl_words

        return (
            join_type(package, type_name),
            is_method,
            is_static,
            is_override)

    def show_panel(self):
        if not hasattr(self, 'output_view'):
            self.output_view = self.window.create_output_panel('usage')

        self.output_view.settings().set('result_file_regex', result_file_regex)
        self.output_view.settings().set(
            'result_base_dir', self.result_base_dir)
        self.output_view.settings().set('line_numbers', False)
        self.output_view.settings().set('gutter', False)
        self.output_view.settings().set('scroll_past_end', False)
        self.output_view.settings().set('draw_centered', False)
        self.output_view.settings().set('word_wrap', False)
        self.output_view.settings().set('rulers', [])
        self.output_view.assign_syntax(
            'Packages/Haxe/Support/HaxeResults.hidden-tmLanguage')

        self.window.create_output_panel('usage')

        self.window.run_command('show_panel', {'panel': 'output.usage'})
