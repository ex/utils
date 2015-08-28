import re
import sublime
import sublime_plugin

try:  # Python 3
    from .haxe_helper import cache
except (ValueError):  # Python 2
    from haxe_helper import cache

header = '''
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
    <key>name</key>
    <string>Globals</string>
    <key>scope</key>
    <string>source.haxe.2</string>
    <key>settings</key>
    <dict>
        <key>shellVariables</key>
        <array>'''

shell_var_template = '''
            <dict>
                <key>name</key>
                <string>{0}</string>
                <key>value</key>
                <string><![CDATA[{1}]]></string>
            </dict>'''

footer = '''
        </array>
    </dict>
    <key>uuid</key>
    <string>0ef292cd-943a-4fb0-b43d-65959c5e6b06</string>
</dict>
</plist>'''

re_format_op_par = re.compile(r'\s*\(\s*')
re_format_cl_par = re.compile(r'\s*\)')
re_format_empty_par = re.compile(r'\(\s+\)')
re_format_colon = re.compile(r'\s*:\s*')
re_format_op_ang = re.compile(r'\s*<\s*')
re_format_cl_ang = re.compile(r'([^-\s])\s*>')
re_format_comma = re.compile(r'\s*,\s*')
re_format_assign = re.compile(r'\s*=\s*')
re_format_type_sep = re.compile(r'\s*->\s*')
re_format_semicolon = re.compile(r'\s*;')
re_format_par_c = re.compile(r'\)\s*:')

re_whitespace_style = re.compile(
    'function f(\s*)\((\s*)'
    'a(\s*):(\s*)T(\s*)<(\s*)T(\s*)>(\s*),(\s*)'
    'b\s*:\s*T(\s*)=(\s*)null(\s*)'
    '\)(\s*):\s*T(\s*)->(\s*)T(\s*);')
re_whitespace_style2 = re.compile(
    'for(\s*)\(\s*i\s+in\s0(\s*)\.\.\.(\s*)5\)')
re_brace_style = re.compile('\}([\s\n]*)else([\s\n]*)\{')

style_map = None
num_tries = 0


def format_statement(view, value):
    global style_map, num_tries

    sm = style_map

    if sm is None and num_tries < 5:
        num_tries += 1
        HaxeFormat.inst.update()
    if sm is None:
        return value

    value = re_format_op_par.sub(
        '%s(%s' % (sm['HX_W_ORB'], sm['HX_ORB_W']), value)
    value = re_format_cl_par.sub('%s)' % sm['HX_W_CRB'], value)
    value = re_format_empty_par.sub('()', value)
    value = re_format_colon.sub(
        '%s:%s' % (sm['HX_W_C'], sm['HX_C_W']), value)
    value = re_format_op_ang.sub(
        '%s<%s' % (sm['HX_W_OAB'], sm['HX_OAB_W']), value)
    value = re_format_cl_ang.sub('\\1%s>' % sm['HX_W_CAB'], value)
    value = re_format_comma.sub(
        '%s,%s' % (sm['HX_W_CM'], sm['HX_CM_W']), value)
    value = re_format_assign.sub(
        '%s=%s' % (sm['HX_W_A'], sm['HX_A_W']), value)
    value = re_format_type_sep.sub(
        '%s->%s' % (sm['HX_W_AR'], sm['HX_AR_W']), value)
    value = re_format_semicolon.sub('%s;' % sm['HX_W_SC'], value)
    value = re_format_par_c.sub(')%s:' % sm['HX_CRB_W_C'], value)

    return value


class HaxeFormat(sublime_plugin.EventListener):

    inst = None

    def __init__(self):
        HaxeFormat.inst = self
        self.changed = False
        self.ws = None
        self.ws2 = None
        self.bs = None
        self.settings = None
        self.init()

    def init(self):
        if sublime.active_window() is None or \
                sublime.active_window().active_view() is None:
            sublime.set_timeout(self.init, 200)
            return

        self.update()

    def mark(self):
        if self.changed:
            return

        self.changed = True

        sublime.set_timeout(self.save_shell_variables, 100)

    def save_shell_variables(self):
        global style_map

        self.changed = False
        s = header

        for key in sorted(style_map.keys()):
            s += shell_var_template.format(key, style_map[key])

        s += footer

        svars = cache('Haxe.ShellVars.tmPreferences')
        if s != svars:
            cache('Haxe.ShellVars.tmPreferences', s)

    def update(self):
        if self.settings is None:
            self.settings = sublime.load_settings('Haxe.sublime-settings')

            self.settings.add_on_change(
                'haxe_whitespace_style',
                lambda: self.update_whitespace_style(self.settings))
            self.settings.add_on_change(
                'haxe_whitespace_style2',
                lambda: self.update_whitespace_style2(self.settings))
            self.settings.add_on_change(
                'haxe_brace_style',
                lambda: self.update_brace_style(self.settings))

        self.update_whitespace_style(self.settings)
        self.update_whitespace_style2(self.settings)
        self.update_brace_style(self.settings)

    def update_brace_style(self, settings):
        global style_map

        def_style = '} else {'
        style = settings.get('haxe_brace_style', def_style)
        if style is None:
            return

        if self.bs is None or self.bs != style:
            self.bs = style

            mo = re_brace_style.search(style)
            if mo is None:
                mo = re_brace_style.search(def_style)

            style_map['HX_CCB_W'] = mo.group(1)  # }_
            style_map['HX_W_OCB'] = mo.group(2)  # _{

            self.mark()

    def update_whitespace_style(self, settings):
        global style_map, settings_map

        def_style = 'function f(a:T<T>, b:T = null):T->T;'
        style = settings.get('haxe_whitespace_style', def_style)
        if style is None:
            return

        if style_map is None:
            style_map = {}
            settings_map = {}

        if self.ws is None or self.ws != style:
            self.ws = style

            mo = re_whitespace_style.search(style)
            if mo is None:
                mo = re_whitespace_style.search(def_style)

            style_map['HX_W_ORB'] = mo.group(1)  # _(
            style_map['HX_ORB_W'] = mo.group(2)  # (_
            style_map['HX_W_C'] = mo.group(3)  # _:
            style_map['HX_C_W'] = mo.group(4)  # :_
            style_map['HX_W_OAB'] = mo.group(5)  # _<
            style_map['HX_OAB_W'] = mo.group(6)  # <_
            style_map['HX_W_CAB'] = mo.group(7)  # _>
            style_map['HX_W_CM'] = mo.group(8)  # _,
            style_map['HX_CM_W'] = mo.group(9)  # ,_
            style_map['HX_W_A'] = mo.group(10)  # _=
            style_map['HX_A_W'] = mo.group(11)  # =_
            style_map['HX_W_CRB'] = mo.group(12)  # _)
            style_map['HX_CRB_W_C'] = mo.group(13)  # ):
            style_map['HX_W_AR'] = mo.group(14)  # _->
            style_map['HX_AR_W'] = mo.group(15)  # ->_
            style_map['HX_W_SC'] = mo.group(16)  # _;

            self.mark()

    def update_whitespace_style2(self, settings):
        global style_map, settings_map

        def_style = 'for (i in 0 ... 5)'
        style = settings.get('haxe_whitespace_style2', def_style)
        if style is None:
            return

        if self.ws2 is None or self.ws2 != style:
            self.ws2 = style

            mo = re_whitespace_style2.search(style)
            if mo is None:
                mo = re_whitespace_style2.search(def_style)

            style_map['HX_K_W_ORB'] = mo.group(1)  # for_(
            style_map['HX_W_TD'] = mo.group(2)  # _...
            style_map['HX_TD_W'] = mo.group(3)  # ..._

            self.mark()
