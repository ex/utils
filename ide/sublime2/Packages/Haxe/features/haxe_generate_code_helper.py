from collections import namedtuple
import sublime
import re

try:  # Python 3
    from .haxe_parse_helper import parse_package
except (ValueError):  # Python 2
    from haxe_parse_helper import parse_package


SCOPE_VAR = 'meta.variable.haxe.2'
SCOPE_VAR_NAME = 'entity.name.variable.haxe.2'
SCOPE_FUNC = 'meta.method.haxe.2'
SCOPE_FUNC_BLOCK = 'meta.method.block.haxe.2'
SCOPE_FUNC_NAME = 'entity.name.function.haxe.2'
SCOPE_PARAMETERS = 'meta.parameters.haxe.2'
SCOPE_STATIC = 'meta.static.haxe.2'
SCOPE_TYPE = 'meta.type'
SCOPE_TYPE_BLOCK = 'meta.type.block.haxe.2'
SCOPE_TYPE_NAME = 'entity.name.type.class.haxe.2'

FIELD_FUNC = 'function'
FIELD_VAR = 'var'
FIELD_STATIC_FUNC = 'static function'
FIELD_STATIC_VAR = 'static var'

re_import = re.compile('^([ \t]*)import\s+([a-z0-9._*]+);', re.I | re.M)
re_prop_params = re.compile(r'\((\w*)\s*,\s*(\w*)\)\s*:?\s*(\w*)')
re_word = re.compile('^[_a-zA-Z]\w*$')


def count_blank_lines(view, pos):
    whitespaces = ' \t'
    src = view.substr(sublime.Region(0, view.size()))
    before, after = 0, 0

    for i in range(pos - 1, 0, -1):
        c = src[i]
        if c == '\n':
            before += 1
        elif c not in whitespaces:
            break

    for i in range(pos, view.size()):
        c = src[i]
        if c == '\n':
            after += 1
        elif c not in whitespaces:
            break

    return before, after


def filter_regions(inners, outers):
    contains = []
    ncontains = []
    ii, io, ni, no = 0, 0, len(inners), len(outers)

    if no == 0:
        return contains, inners[:]

    while io < no and ii < ni:
        inner = inners[ii]
        outer = outers[io]

        if outer.contains(inner):
            contains.append(inner)
            io += 1
            ii += 1
            continue

        if inner.begin() > outer.begin():
            io += 1
        else:
            ncontains.append(inner)
            ii += 1

    while ii < ni:
        ncontains.append(inners[ii])
        ii += 1

    return contains, ncontains


def find_cur_region(view, selector, as_string=False):
    rgns = view.find_by_selector(selector)
    pos = view.sel()[0].begin()

    for rgn in rgns:
        if rgn.contains(pos):
            if as_string:
                return view.substr(rgn)
            else:
                return rgn

    return None


def find_line_start_pos(view, pos):
    rgn = view.line(pos)
    pos = rgn.begin()
    line = view.substr(rgn)
    for c in line:
        if c == ' ' or c == '\t':
            pos += 1
        else:
            break

    return pos


def find_regions(view, selector, in_region=None, incl_string=False):
    rgns = view.find_by_selector(selector)
    regions = []

    for rgn in rgns:
        if in_region is not None and in_region.contains(rgn):
            if incl_string:
                regions.append((rgn, view.substr(rgn)))
            else:
                regions.append(rgn)

    return regions


def get_blank_lines(view, name, default=0):
    n = view.settings().get(name, default)
    return '\n' * n


def get_context(view):
    return HaxeContext(view)


def get_default_value(type_name):
    if type_name == 'Float' or type_name == 'Int':
        return '0'
    elif type_name == 'Void':
        return None
    elif type_name == 'Bool':
        return 'false'

    return 'null'


def get_mod_order(view):
    def_order = 'opis'
    order = view.settings().get('haxe_modifiers_order', def_order)

    for c in def_order:
        if c not in order:
            order += c

    return order


def get_mods(view, private=True, o=False, p=True, i=False, s=True):
    mods = ''
    mod_map = {}

    order = get_mod_order(view)

    def add_mod(use, key, value):
        if use:
            mod_map[key] = value

    add_mod(o, 'o', 'override')
    add_mod(p, 'p', 'private' if private else 'public')
    add_mod(i, 'i', 'inline')
    add_mod(s, 's', 'static')

    for c in order:
        if c not in mod_map:
            continue
        mods += mod_map[c] + ' '
        del mod_map[c]

    return mods.strip()


def get_editable_mods(
        view, idx,
        private=True, o=False, p=True, i=False, s=True,
        eo=False, ep=False, ei=False, es=False):
    mods = []
    mod_map = {}
    edit_map = {}

    order = get_mod_order(view)

    def add_mod(use, key, value, editable):
        edit_map[key] = editable
        if use:
            mod_map[key] = value

    add_mod(o, 'o', 'override', eo)
    add_mod(p, 'p', 'private' if private else 'public', ep)
    add_mod(i, 'i', 'inline', ei)
    add_mod(s, 's', 'static', es)

    for c in order:
        if c not in mod_map:
            continue
        mod = mod_map[c] + ' '
        if edit_map[c]:
            mod = '${%d:%s }' % (idx, mod_map[c])
            idx += 1
        mods.append(mod)
        del mod_map[c]

    return ''.join(mods)


def is_haxe_scope(view):
    return view.score_selector(0, "source.haxe.2") > 0


def is_imported(tp, imports):
    for itp in imports:
        itp = itp.strip('.*')
        if itp == tp:
            return True
        if itp in tp:
            rtp = tp.replace(itp, '')
            if rtp.count('.') == 1:
                return True

    return False


def set_pos(view, pos, center=True):
    view.sel().clear()
    view.sel().add(sublime.Region(pos, pos))
    if center:
        view.show_at_center(pos)


def shorten_imported_type(tp, imports):
    if '.' in tp:
        if is_imported(tp, imports):
            tp = tp.rpartition('.')[2]

    return tp


CtxVar = namedtuple('CtxVar', ['group', 'name', 'region'])
CtxMethod = namedtuple('CtxMethod', ['group', 'name', 'region', 'block'])
CtxType = namedtuple(
    'CtxType',
    ['group', 'name', 'package', 'full_name', 'region', 'block',
        'vars', 'svars', 'methods', 'smethods', 'field_map'])
CtxWord = namedtuple('CtxWord', ['name', 'region', 'scope'])


class HaxeContext(object):

    def __init__(self, view):
        super(HaxeContext, self).__init__()
        self.view = view
        pos = view.sel()[0].begin()
        self.scope = view.scope_name(pos)
        self._type = None
        self._var = None
        self._method = None
        self._word = None
        self._src = None
        self._imports = None

    def get_imports(self):
        if self._imports is None:
            self._imports = \
                [mo.group(2) for mo in re_import.finditer(self.src)]

        return self._imports

    def get_method(self):
        if self._method is None:
            self._method = False

            if SCOPE_FUNC not in self.scope:
                return False

            rgn = find_cur_region(self.view, SCOPE_FUNC)
            self._method = CtxMethod(
                FIELD_STATIC_FUNC if SCOPE_STATIC in self.scope else
                FIELD_FUNC,
                find_regions(self.view, SCOPE_FUNC_NAME, rgn, True)[0][1],
                rgn,
                find_regions(self.view, SCOPE_FUNC_BLOCK, rgn)[0])

        return self._method

    def get_src(self):
        if self._src is None:
            self._src = self.view.substr(sublime.Region(0, self.view.size()))

        return self._src

    def get_type(self):
        if self._type is None:
            self._type = False

            if SCOPE_TYPE not in self.scope:
                return False

            view = self.view
            type_group = None
            type_scope = None
            type_groups = ('abstract', 'class', 'enum', 'interface', 'typedef')

            for group in type_groups:
                type_scope = 'meta.type.%s.haxe.2' % group
                if type_scope in self.scope:
                    type_group = group
                    break

            type_rgn = find_cur_region(view, type_scope)

            v_rgns = find_regions(view, SCOPE_VAR, type_rgn)
            vname_rgns = find_regions(view, SCOPE_VAR_NAME, type_rgn)
            f_rgns = find_regions(view, SCOPE_FUNC, type_rgn)
            fname_rgns = find_regions(view, SCOPE_FUNC_NAME, type_rgn)
            s_rgns = find_regions(view, SCOPE_STATIC, type_rgn)

            sv_rgns, v_rgns = filter_regions(v_rgns, s_rgns)
            sf_rgns, f_rgns = filter_regions(f_rgns, s_rgns)

            svname_rgns, vname_rgns = filter_regions(vname_rgns, sv_rgns)
            sfname_rgns, fname_rgns = filter_regions(fname_rgns, sf_rgns)

            def combine(field_group, field_rgns, field_name_rgns):
                lst = []
                is_var = 'var' in field_group

                for i in range(0, len(field_rgns)):
                    ctx = None
                    if is_var:
                        ctx = CtxVar(
                            field_group,
                            view.substr(field_name_rgns[i]),
                            field_rgns[i])
                    else:
                        ctx = CtxMethod(
                            field_group,
                            view.substr(field_name_rgns[i]),
                            field_rgns[i],
                            find_regions(
                                view, SCOPE_FUNC_BLOCK, field_rgns[i])[0])
                    lst.append(ctx)

                return lst

            v_ctxs = combine(FIELD_VAR, v_rgns, vname_rgns)
            sv_ctxs = combine(FIELD_STATIC_VAR, sv_rgns, svname_rgns)
            f_ctxs = combine(FIELD_FUNC, f_rgns, fname_rgns)
            sf_ctxs = combine(FIELD_STATIC_FUNC, sf_rgns, sfname_rgns)

            field_map = {}
            for ctx in v_ctxs:
                field_map[ctx.name] = ctx
            for ctx in sv_ctxs:
                field_map[ctx.name] = ctx
            for ctx in f_ctxs:
                field_map[ctx.name] = ctx
            for ctx in sf_ctxs:
                field_map[ctx.name] = ctx

            name = find_regions(view, SCOPE_TYPE_NAME, type_rgn, True)[0][1]
            package = parse_package(self.src)

            full_name = name
            if package:
                full_name = package + '.' + name

            self._type = CtxType(
                type_group,
                name,
                package,
                full_name,
                type_rgn,
                find_regions(view, SCOPE_TYPE_BLOCK, type_rgn)[0],
                v_ctxs,
                sv_ctxs,
                f_ctxs,
                sf_ctxs,
                field_map)

        return self._type

    def get_var(self):
        if self._var is None:
            self._var = False

            if SCOPE_VAR not in self.scope:
                return False

            rgn = find_cur_region(self.view, SCOPE_VAR)
            self._var = CtxVar(
                FIELD_STATIC_VAR if SCOPE_STATIC in self.scope else FIELD_VAR,
                find_regions(self.view, SCOPE_VAR_NAME, rgn, True)[0][1],
                rgn)

        return self._var

    def get_word(self):
        if self._word is None:
            self._word = False

            view = self.view
            pos = view.sel()[0].begin()
            word_rgn = view.word(pos)
            word = view.substr(word_rgn)
            scope = view.scope_name(word_rgn.begin())

            if not re_word.match(word):
                return False

            ignore_scopes = (
                'comment', 'constant', 'keyword', 'storage', 'string')

            for sc in ignore_scopes:
                if sc in scope:
                    return False

            self._word = CtxWord(word, word_rgn, scope)

        return self._word

    method = property(get_method)
    type = property(get_type)
    var = property(get_var)
    word = property(get_word)
    src = property(get_src)
    imports = property(get_imports)
