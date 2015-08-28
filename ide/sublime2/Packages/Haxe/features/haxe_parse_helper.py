import os
import re

re_class = re.compile((
    r'class\s+(\w+)(?:\s*<[\w\.,\s]+>)?'
    r'(?:\s+implements\s+(?:[\w\.]+)(?:\s*<[\w\.,\s]+>)?)*'
    r'(?:\s+extends\s+([\w\.]+)(?:\s*<[\w\.,\s]+>)?)?'
    r'(?:\s+implements\s+(?:[\w\.]+)(?:\s*<[\w\.,\s]+>)?)*'
    ), re.M)
re_comments = re.compile(
    r'(//[^\n\r]*?[\n\r]|/\*(.*?)\*/)', re.MULTILINE | re.DOTALL)
re_import = re.compile(r'import\s+([\w\.*]+)[^;]*;', re.MULTILINE)
re_package = re.compile(r'package\s*([a-z0-9.]*);', re.I | re.M)
re_type_decl = re.compile(
    r'(?:abstract|class|interface|enum|typedef)\s+(\w+)', re.M)


def find_class_declarations(src):
    return [mo for mo in re_class.finditer(src)]


def find_comment_regions(src):
    regions = []
    for mo in re_comments.finditer(src):
        regions.append((mo.start(0), mo.end(0)))
    return regions


def find_field_declaration(src, field_name, type_name=None):
    mo = re.search(
        r'((?:override|static|macro|inline|public|private|#if.*?#end)\s+)*'
        r'(?:(?:var|function))\s+%s' % field_name,
        src)
    if mo:
        return mo.group(0)

    return None


def find_type_path(type_name, type_map, imported_type_map, package_path):
    if '.' in type_name:
        return type_name

    if type_name in type_map:
        package = type_map[type_name]

        if is_string(package):
            return join_type(package, type_name)
        else:
            for p in package:
                if p == '':
                    continue

                for imp in imported_type_map:
                    if imp == '*':
                        continue
                    print(p, imp, imported_type_map[imp])
                    if p == imported_type_map[imp].rpartition('.')[0]:
                        return join_type(p, type_name)

            if '*' in imported_type_map:
                for imp in imported_type_map['*']:
                    imp_pk = imp.rpartition('.')[0]
                    for p in package:
                        if p == imp_pk:
                            return join_type(p, type_name)

            if package_path in package:
                return join_type(package_path, type_name)

            if '' in package:
                return type_name

    return None


def find_line_positions(src):
    lines = src.split('\n')
    pos = 0
    positions = []
    for line in lines:
        pos += len(line) + 1
        positions.append(pos)
    return positions


def find_module_filepath(type_name, classpaths):
    rel_module_filepath = to_module_filepath(type_name)

    for cp in classpaths:
        if not cp:
            continue
        module_filepath = os.path.join(cp, rel_module_filepath)
        if os.path.isfile(module_filepath):
            return module_filepath
    return None


def get_package(path):
    parts = path.split('.')
    if parts and not is_type(parts[-1]):
        parts.pop()
    if len(parts) > 1 and is_type(parts[-1]) and is_type(parts[-2]):
        parts.pop()
    if parts and is_type(parts[-1]):
        parts.pop()
    return '.'.join(parts)


def get_parent_path(path):
    return path.rpartition('.')[0]


def has_module_in_path(type_path):
    parts = type_path.split('.')
    return len(parts) > 1 and is_type(parts[-1]) and is_type(parts[-2])


def is_imported(type_paths, type_map, imported_type_map, all=True):
    for type_path in type_paths:
        type_pk, _, type_name = type_path.rpartition('.')

        if has_module_in_path(type_path):
            type_paths.append(type_path.rpartition('.')[0])

        if type_name in imported_type_map and \
                imported_type_map[type_name] == type_path:
            if not all:
                return True
            continue

        tp_is_imported = False

        if '*' in imported_type_map:
            package = type_map[type_name]

            if is_string(package):
                tp_is_imported = package in imported_type_map['*']
            else:
                for imp in imported_type_map['*']:
                    imp_pk = imp.rpartition('.')[0]
                    for p in package:
                        if p == type_pk and p == imp_pk:
                            tp_is_imported = True
                            break
                    if tp_is_imported:
                        break

        if not tp_is_imported and all:
            return False
        if tp_is_imported and not all:
            return True

    return all


def is_in_package(type_path, package):
    type_package = get_package(type_path)
    return type_package == package


def is_string(value):
    val = False
    try:
        val = isinstance(value, basestring)
    except:
        val = isinstance(value, str)

    return val


def is_type(type_name, type_map=None):
    c = type_name[0]
    result = c != '_' and c.upper() == c

    if result and type_map:
        result = type_name in type_map

    return result


def join_type(package, type_name):
    if package:
        type_name = package + '.' + type_name

    return type_name


def parse_declared_type_names(src, as_dict):
    lst = None if as_dict else []
    dct = {} if as_dict else None

    for mo in re_type_decl.finditer(src):
        if as_dict:
            dct[mo.group(1)] = True
        else:
            lst.append(mo.group(1))

    return dct if as_dict else lst


def parse_imports(src, as_dict=False):
    lst = None if as_dict else []
    dct = {} if as_dict else None

    for mo in re_import.finditer(src):
        imp_path = mo.group(1)
        if as_dict:
            imp_name = imp_path.rpartition('.')[2]
            if imp_name == '*':
                if imp_name in dct:
                    dct[imp_name].append(imp_path)
                else:
                    dct[imp_name] = [imp_path]
            else:
                dct[imp_name] = imp_path
        else:
            lst.append(imp_path)

    return dct if as_dict else lst


def parse_package(src):
    mo = re_package.search(src)
    if mo:
        return mo.group(1)
    return ''


def remove_comments(text):
    return re_comments.sub('', text)


def to_module_filepath(type_path):
    if has_module_in_path(type_path):
        type_path = type_path.rpartition('.')[0]

    path = os.sep.join(type_path.split('.'))
    return '%s.hx' % path
