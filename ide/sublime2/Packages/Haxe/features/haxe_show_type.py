import codecs
import re
import sublime
import sublime_plugin

try:  # Python 3
    from .haxe_helper import HaxeComplete_inst
    from .haxe_format import format_statement
except (ValueError):  # Python 2
    from haxe_helper import HaxeComplete_inst
    from haxe_format import format_statement


re_params = re.compile(r'\b(\w*)(\s*):')


class HaxeShowType(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view

        if view.score_selector(0, 'source.haxe.2') == 0 or \
                int(sublime.version()) < 3000:
            return

        # get word under cursor
        word = view.word(view.sel()[0])

        # get utf-8 byte offset to the end of the word
        src = view.substr(sublime.Region(0, word.b))
        offset = len(codecs.encode(src, "utf-8")) + 1
        # add 1 because offset is 1-based

        complete = HaxeComplete_inst()

        # save file and run completion
        temp = complete.save_temp_file(view)
        hint = complete.run_haxe(view, dict(
            mode="type",
            filename=view.file_name(),
            offset=offset,
            commas=None
        ))
        complete.clear_temp_file(view, temp)

        if hint is None:
            status = "No type information for '%s'." % \
                view.substr(sublime.Region(word.a, word.b))
            view.set_status("haxe-status", status)
        else:
            hint = format_statement(view, hint)
            view.set_status("haxe-status", hint)

            hint = hint.replace('<', '&lt;')
            hint = hint.replace('>', '&gt;')
            hint = re_params.sub(r'<b>\1</b>\2:', hint)

            if int(sublime.version()) >= 3070 and \
                    view.settings().get("haxe_use_popup", True):
                view.run_command('haxe_show_popup', {'text': hint})
            else:
                view.show_popup_menu([hint], lambda i: None)
