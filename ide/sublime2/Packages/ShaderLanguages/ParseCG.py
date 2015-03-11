import sublime
import sublime_plugin
import re
from subprocess import Popen, PIPE

#Derivated from the Lua Dev package: https://github.com/rorydriscoll/LuaSublime

s = sublime.load_settings("ShaderLanguages.sublime-settings")

class ParseCGCommand(sublime_plugin.EventListener):

	TIMEOUT_MS = 200

	def __init__(self):
		self.pending = 0

	def on_modified(self, view):
		if not s.get("live_parser"):
			return
		filename = view.file_name()
		if not filename or not filename.endswith('.cg'):
			return
		self.pending = self.pending + 1
		sublime.set_timeout(lambda: self.parse(view), self.TIMEOUT_MS)

	def parse(self, view):
		# Don't bother parsing if there's another parse command pending
		self.pending = self.pending - 1
		if self.pending > 0:
			return
		# Grab the path to cgc from the settings
		cgc_path = s.get("cgc_path")

		# Run cgc with the parse option
		p = Popen(cgc_path + ' -noentry ', stdin=PIPE, stderr=PIPE, shell=True)
		text = view.substr(sublime.Region(0, view.size()))
		errors = p.communicate(text.encode('utf-8'))[1]
		result = p.wait()
		# Clear out any old region markers
		view.erase_regions('cgerrors')
		view.erase_regions('cgwarnings')

		# Add warning regions and place the error message in the status bar
		sublime.status_message(errors)
		pattern = re.compile(r'\(([0-9]+)\) \: warning')

		warnings = [view.full_line(view.text_point(int(match.group( 1 )) - 1, 0)) for match in pattern.finditer(errors)]
		view.add_regions('cgwarnings', warnings, 'warning', 'DOT', sublime.HIDDEN)
		
		# Add error regions and place the error message in the status bar
		pattern = re.compile(r'\(([0-9]+)\) \: error')
		errors = [view.full_line(view.text_point(int(match.group( 1 )) - 1, 0)) for match in pattern.finditer(errors)]
		view.add_regions('cgerrors', errors, 'invalid', 'DOT', sublime.HIDDEN)
