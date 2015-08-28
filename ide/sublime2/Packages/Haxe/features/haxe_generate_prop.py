import re
import sublime_plugin

try:  # Python 3
    from .haxe_generate_code_helper import *
except (ValueError):  # Python 2
    from haxe_generate_code_helper import *


class HaxeGenerateGetSet(sublime_plugin.WindowCommand):

    @staticmethod
    def poll(ctx):
        view = ctx.view
        cmds = []

        if not ctx.type or ctx.type.group != 'class':
            return cmds

        if ctx.var:
            mo = re_prop_params.search(view.substr(ctx.var.region))
            if not mo:
                return cmds
            if mo.group(1) and mo.group(1).find('get') == 0 and \
                    'get_' + ctx.var.name not in ctx.type.field_map or \
                    mo.group(2) and mo.group(2).find('set') == 0 and \
                    'set_' + ctx.var.name not in ctx.type.field_map:

                cmds.append((
                    'Generate Getter And Setter',
                    'haxe_generate_get_set',
                    {}))

        return cmds

    def run(self):
        view = self.window.active_view()

        if view is None or view.is_loading() or not is_haxe_scope(view):
            return

        ctx = get_context(view)
        self.context = ctx

        if not ctx.type or ctx.type.group != 'class' or not ctx.var:
            return

        prop_name = ctx.var.name
        get_name = 'get_' + prop_name
        set_name = 'set_' + prop_name
        prop_var_name = '_' + prop_name
        group_prop = view.settings().get(
            'haxe_group_property_and_accessors', True)

        post_blank_lines = ''
        pre_blank_lines = ''
        bl_group = get_blank_lines(view, 'haxe_bl_group')
        if group_prop:
            post_blank_lines = get_blank_lines(view, 'haxe_bl_property')
            pre_blank_lines = '\n' + post_blank_lines

        mo = re_prop_params.search(view.substr(ctx.var.region))
        ret = 'Dynamic'
        if mo.group(3):
            ret = mo.group(3)
        val = get_default_value(ret)
        is_static = ctx.var.group == FIELD_STATIC_VAR
        mods = get_mods(
            view, True, False, True, False, is_static)
        ftype = FIELD_STATIC_FUNC if is_static else FIELD_FUNC

        set_aid = mo.group(2)
        setter = set_aid and set_aid.find('set') == 0 and \
            set_name not in ctx.type.field_map
        get_aid = mo.group(1)
        getter = get_aid and get_aid.find('get') == 0 and \
            get_name not in ctx.type.field_map

        if setter:
            pos = ctx.var.region.end()
            if get_name in ctx.type.field_map:
                pos = ctx.type.field_map[get_name][2].end()
            if prop_var_name in ctx.type.field_map:
                text_set = '\t%s$HX_W_A=${HX_A_W}value$HX_W_SC;\n' % (
                    prop_var_name)
                val = prop_var_name
            elif get_aid == 'default':
                text_set = '\t%s$HX_W_A=${HX_A_W}value$HX_W_SC;\n' % (
                    prop_name)
                val = prop_name
            else:
                text_set = ''
                val = 'value'
            text = (
                '%s'
                '%s function %s$HX_W_ORB(${HX_ORB_W}'
                'value$HX_W_C:${HX_C_W}%s$HX_W_CRB)$HX_CRB_W_C:${HX_C_W}%s'
                '$HX_W_OCB{\n%s\treturn %s$HX_W_SC;\n}%s')
            text = text % (
                pre_blank_lines, mods, set_name, ret, ret, text_set, val,
                bl_group)

            if group_prop:
                self.window.run_command(
                    'haxe_generate_field_edit',
                    {'pos': pos, 'text': text, 'move': False})
            else:
                self.window.run_command(
                    'haxe_generate_field',
                    {'name': set_name, 'field': ftype, 'text': text})

        if getter:
            pos = ctx.var.region.end()
            if set_name not in ctx.type.field_map and not setter:
                post_blank_lines = bl_group
            if prop_var_name in ctx.type.field_map:
                val = prop_var_name
            text = (
                '%s'
                '%s function %s$HX_W_ORB()$HX_CRB_W_C:${HX_C_W}%s'
                '$HX_W_OCB{\n\treturn %s$HX_W_SC;\n}%s')
            text = text % (
                pre_blank_lines, mods, get_name, ret, val, post_blank_lines)

            if group_prop:
                self.window.run_command(
                    'haxe_generate_field_edit',
                    {'pos': pos, 'text': text, 'move': False})
            else:
                self.window.run_command(
                    'haxe_generate_field',
                    {'name': get_name, 'field': ftype, 'text': text})


class HaxeConvertToProp(sublime_plugin.TextCommand):

    def find_insert_pos(self, prop_name):
        ctx = self.context
        view = ctx.view

        var = ctx.type.field_map[prop_name]
        var_region = var.region

        name_region = find_regions(
            view, SCOPE_VAR_NAME, var_region)[0]
        erase_region = sublime.Region(name_region.end(), var_region.end())
        src = view.substr(erase_region)
        mo = re.search(r'^(\s*)(:?)', src, re.M)
        erase_region = sublime.Region(
            erase_region.a, erase_region.a + len(mo.group(1)))

        return name_region.end(), erase_region, mo.group(2) is not None

    @staticmethod
    def poll(ctx):
        view = ctx.view
        cmds = []

        if not ctx.type or ctx.type.group != 'class':
            return cmds

        if ctx.word and ctx.word.name in ctx.type.field_map:
            var = ctx.type.field_map[ctx.word.name]
            if 'var' in var.group:
                mo = re_prop_params.search(view.substr(var.region))
                if not mo:
                    cmds.append((
                        'Convert To Property',
                        'haxe_convert_to_prop',
                        {}))

        return cmds

    def run(self, edit):
        view = self.view

        if view is None or view.is_loading() or not is_haxe_scope(view):
            return

        ctx = get_context(view)
        self.context = ctx

        if not ctx.type or ctx.type.group != 'class':
            return

        pos, erase_region, has_ret = self.find_insert_pos(ctx.word.name)
        text = (
            '$HX_W_ORB($HX_ORB_W${1:get}'
            '$HX_W_CM,$HX_CM_W'
            '${2:set}$HX_W_CRB)')
        if has_ret:
            text += '$HX_CRB_W_C'

        if not erase_region.empty():
            view.erase(edit, erase_region)
        set_pos(view, pos)
        view.run_command('insert_snippet', {"contents": text})


class HaxeGeneratePropVar():

    @staticmethod
    def poll(ctx):
        view = ctx.view
        cmds = []

        if not ctx.type or ctx.type.group != 'class':
            return cmds

        prop = None
        mo = None

        if ctx.var:
            mo = re_prop_params.search(view.substr(ctx.var.region))
            if mo:
                prop = ctx.var
        elif ctx.word:
            if ctx.word.name in ctx.type.field_map:
                var = ctx.type.field_map[ctx.word.name]
                mo = re_prop_params.search(view.substr(var.region))
                if mo:
                    prop = var

        if prop:
            fname = '_' + prop[1]
            fgroup = prop[0]
            caption = 'Add var ' + fname
            if fgroup == FIELD_STATIC_VAR:
                caption = 'Add static var ' + fname
            if fname not in ctx.type.field_map:
                ret = 'Dynamic'
                if mo.group(3):
                    ret = mo.group(3)
                mods = get_mods(
                    view, True, False, True, False,
                    prop[0] == FIELD_STATIC_VAR)
                text = '%s var %s$HX_W_C:${HX_C_W}%s$HX_W_SC;' % (
                    mods, fname, ret)
                cmds.append((
                    caption,
                    'haxe_generate_field',
                    {'name': fname, 'field': fgroup, 'text': text}))

        return cmds
