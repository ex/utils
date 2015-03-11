import codecs
import sublime
import sublime_plugin

try: # Python 3
    from ..HaxeHelper import HaxeComplete_inst
except (ValueError): # Python 2
    from HaxeHelper import HaxeComplete_inst

class HaxeShowType( sublime_plugin.TextCommand ):

    def run( self , edit ) :

        view = self.view

        # get word under cursor
        word = view.word(view.sel()[0])

        # get utf-8 byte offset to the end of the word
        src = view.substr(sublime.Region(0, word.b))
        offset = len(codecs.encode(src, "utf-8")) + 1 # add 1 because offset is 1-based

        complete = HaxeComplete_inst()

        # save file and run completion
        temp = complete.save_temp_file( view )
        hint = complete.run_haxe(view, dict(
            mode="type",
            filename=view.file_name(),
            offset=offset,
            commas=None
        ))
        complete.clear_temp_file( view , temp )

        if hint is None:
            status = "No type information for '" + view.substr(sublime.Region(word.a, word.b)) + "'."
            self.view.set_status( "haxe-status", status )
        else :
            self.view.show_popup_menu([hint], lambda i: None)
            self.view.set_status( "haxe-status", hint )
