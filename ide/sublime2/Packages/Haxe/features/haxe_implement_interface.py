import codecs
import os.path
import re
import sublime_plugin

try:  # Python 3
    from .haxe_generate_code_helper import *
    from .haxe_organize_imports import HaxeOrganizeImports
    from .haxe_helper import HaxeComplete_inst, get_classpaths
    from .haxe_parse_helper import *
except (ValueError):  # Python 2
    from haxe_generate_code_helper import *
    from haxe_organize_imports import HaxeOrganizeImports
    from haxe_helper import HaxeComplete_inst, get_classpaths
    from haxe_parse_helper import *

re_implements = re.compile(r'implements\s+([\w\.]+)', re.MULTILINE)
re_field = re.compile(r'(var|function)\s+(\w+)[^;]*;', re.MULTILINE)
re_return = re.compile(r'\)\s*:\s*([\w\.<>-]+);', re.MULTILINE)


def is_full_path(path):
    return '.' in path


class HaxeImplementInterface(sublime_plugin.WindowCommand):

    def extract_fields(self, src):
        lst = []
        if src is None:
            return lst

        for mo in re_field.finditer(src):
            name = mo.group(2)
            if name in self.context.type.field_map:
                continue
            lst.append((mo.group(1), name, 'public ' + mo.group(0)))

        return lst

    def extract_type(self, src, start):
        br_begin = 0
        for i in range(start, len(src)):
            c = src[i]
            if c == '{':
                br_begin += 1
            elif c == '}':
                if br_begin == 0:
                    return src[start:i]
                br_begin -= 1

        return None

    def find_fields(self):
        extends = []

        for iface in self.interfaces:
            s = codecs.open(iface[2], "r", "utf-8", "ignore")
            src = remove_comments(s.read())
            imp_map = parse_imports(src, True)
            pat = 'interface\s+%s\s+(extends\s+([\w.]+))?\s*\{' % iface[0]
            mo = re.search(pat, src, re.MULTILINE)
            if mo:
                pos = mo.end(0)
                src_type = self.extract_type(src, pos)
                self.fields_to_insert.extend(self.extract_fields(src_type))

                if mo.group(2):
                    # exname, ex = self.split_type(mo.group(2), imp_map)
                    full_type_name = find_full_type_name(
                        mo.group(2), self.type_map, imp_map)

                    if full_type_name is None:
                        # error
                        continue

                    type_name = full_type_name.rpartition('.')[2]

                    if type_name not in self.parsed_iname_map:
                        extends.append(
                            (type_name, to_module_filepath(full_type_name)))

        if extends:
            self.interfaces = extends
            self.find_files()
            self.find_fields()

    def find_files(self):
        lst = []

        for iface in self.interfaces:
            iname = iface[0]
            ipath = iface[1]
            self.parsed_iname_map[iname] = True
            ifile = ''
            for cp in self.classpaths:
                if not cp:
                    continue
                fl = os.path.join(cp, ipath)
                if os.path.isfile(fl):
                    ifile = fl
                    break
            if ifile:
                lst.append((iname, ipath, ifile))

        print('files', lst)
        self.interfaces = lst

    def find_interfaces(self):
        ctx = self.context
        view = self.window.active_view()
        src = view.substr(ctx.type.region)
        self.interfaces = []
        ifaces = []
        imp_map = parse_imports(remove_comments(self.context.src), True)

        for mo in re_implements.finditer(src):
            ifaces.append(mo.group(1))

        print(ifaces)
        for iface in ifaces:
            # type_name, type_path = self.split_type(iface, imp_map)
            full_type_name = find_full_type_name(iface, self.type_map, imp_map)

            if full_type_name is None:
                # error
                continue

            self.interfaces.append((
                full_type_name.rpartition('.')[2],
                to_module_filepath(full_type_name)))
        print(self.interfaces)

    # def get_module_file_path(self, type_name, type_path):
    #     if is_package(type_path):
    #         type_path += '.' + type_name
    #     stype_path = type_path.split('.')
    #     if len(stype_path) > 1 and \
    #             is_type(stype_path[-1]) and is_type(stype_path[-2]):
    #         stype_path.pop()
    #     path = os.path.join(*stype_path)
    #     return '%s.hx' % path

    def insert_fields(self):
        for field in self.fields_to_insert:
            ftype = field[0]
            fname = field[1]
            ftext = field[2]
            if ftype == FIELD_FUNC:
                ret = ''
                mo = re_return.search(ftext)
                if mo:
                    ret_val = get_default_value(mo.group(1))
                    if ret_val:
                        ret = 'return %s;' % ret_val
                ftext = ftext.replace(
                    ';', '$HX_W_OCB{\n\t%s\n}' % ret)

            self.window.run_command(
                'haxe_generate_field',
                {'name': fname, 'field': ftype, 'text': ftext})

    @staticmethod
    def poll(ctx):
        if not ctx.type or ctx.type.group != 'class':
            return []

        view = ctx.view
        src = view.substr(ctx.type.region)
        if re_implements.search(src) is None:
            return []

        cmds = []

        cmds.append((
            'Implement Interface',
            'haxe_implement_interface',
            {}))

        return cmds

    def run(self):
        win = self.window
        view = win.active_view()

        if view is None or view.is_loading() or not is_haxe_scope(view):
            return

        self.context = get_context(view)
        self.classpaths = get_classpaths(view)

        if not self.context.type:
            return

        self.type_map = HaxeOrganizeImports.get_type_map(view)
        if self.type_map is None:
            return

        self.parsed_iname_map = {}
        self.fields_to_insert = []

        self.find_interfaces()
        self.find_files()
        self.find_fields()
        self.insert_fields()
