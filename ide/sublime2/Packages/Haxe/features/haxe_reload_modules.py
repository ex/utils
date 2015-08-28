import sublime
import sys

if sys.version_info >= (3,):
    from imp import reload

haxe_modules = []
for mod in sys.modules:
    if 'haxe_' in mod and sys.modules[mod] != None:
        haxe_modules.append(mod)

package = 'features'
if int(sublime.version()) >= 3000:
    package = 'Haxe.' + package

submods = [
    '',
    '.haxe_helper',
    '.haxe_errors',
    '.haxe_generate_code_helper',
    '.haxe_format',
    '.haxe_hint',
    '.haxe_organize_imports',
    '.haxe_generate_field',
    '.haxe_restart_server',
    '.haxe_create_type',
    '.haxe_generate_import',
    '.haxe_find_definition',
    '.haxe_show_type',
    '.haxe_add_hxml',
    '.haxe_extract_var',
    '.haxe_implement_interface',
    '.haxe_generate_code',
    '.haxe_reload_modules',
]


def reload_modules():
    print('Reload submods')
    for submod in submods:
        mod = package + submod
        if mod in haxe_modules:
            try:
                reload(sys.modules[mod])
            except:
                pass
