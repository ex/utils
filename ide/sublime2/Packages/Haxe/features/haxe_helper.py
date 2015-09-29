import sys, sublime, sublime_plugin
import subprocess, time
import os, signal
import errno

from subprocess import Popen, PIPE
from datetime import datetime

import threading
import traceback
import shlex
import re


def HaxeComplete_inst():
    try:  # Python 3
        from ..HaxeComplete import HaxeComplete
    except (ValueError):  # Python 2
        from HaxeComplete import HaxeComplete
    return HaxeComplete.inst

spaceChars = re.compile("\s")
wordChars = re.compile("[a-z0-9._]", re.I)
importLine = re.compile("^([ \t]*)import\s+([a-z0-9._*]+);", re.I | re.M)
packageLine = re.compile("package\s*([a-z0-9.]*);", re.I)

compactFunc = re.compile("\(.*\)")
compactProp = re.compile(":.*\.([a-z_0-9]+)", re.I)
libLine = re.compile("([^:]*):[^\[]*\[(dev\:)?(.*)\]")
classpathLine = re.compile("Classpath : (.*)")
typeDecl = re.compile("(class|interface|enum|typedef|abstract)\s+([A-Z][a-zA-Z0-9_]*)\s*(<[a-zA-Z0-9_,]+>)?" , re.M )
libFlag = re.compile("-lib\s+(.*?)")
skippable = re.compile("^[a-zA-Z0-9_\s]*$")
inAnonymous = re.compile("[{,]\s*([a-zA-Z0-9_\"\']+)\s*:\s*$" , re.M | re.U )
extractTag = re.compile("<([a-z0-9_-]+).*\s(name|main|path)=\"([a-z0-9_./-]+)\"", re.I)
extractTagName = re.compile("<([a-z0-9_-]+).*\s", re.I)
variables = re.compile("var\s+([^:;(\s]*)", re.I)
functions = re.compile("function\s+([^;\.\(\)\s]*)", re.I)
functionParams = re.compile("function\s+[a-zA-Z0-9_]+\s*\(([^\)]*)", re.M)
paramDefault = re.compile("(=\s*\"*[^\"]*\")", re.M)
isType = re.compile("^[A-Z][a-zA-Z0-9_]*$")
comments = re.compile("(//[^\n\r]*?[\n\r]|/\*(.*?)\*/)", re.MULTILINE | re.DOTALL )

haxeVersion = re.compile("(Haxe|haXe) Compiler (([0-9]\.[0-9])\.?[0-9]?)",re.M)
haxeFileRegex = "^(.+):(\\d+): (?:lines \\d+-\\d+|character(?:s \\d+-| )(\\d+)) : (.*)$"
controlStruct = re.compile( "\s*(if|switch|for|while)\s*\($" );


try:
  STARTUP_INFO = subprocess.STARTUPINFO()
  STARTUP_INFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW
  STARTUP_INFO.wShowWindow = subprocess.SW_HIDE
except (AttributeError):
    STARTUP_INFO = None

try :
    stexec = __import__("exec")
    ExecCommand = stexec.ExecCommand
    AsyncProcess = stexec.AsyncProcess
except ImportError as e :
    import Default
    stexec = getattr( Default , "exec" )
    ExecCommand = stexec.ExecCommand
    AsyncProcess = stexec.AsyncProcess
    unicode = str #dirty...

def cache(filename, data=None):
    cache_dir = os.path.join(
        sublime.packages_path(), 'User', 'Haxe.cache')
    cache_file = os.path.join(cache_dir, filename)

    if not os.path.exists(cache_dir):
        try:
            os.makedirs(cache_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                return None

    # read
    if data is None:
        try:
            f = open(cache_file, 'r')
            data = f.read()
            f.close()
            return data
        except:
            return None

    # write
    try:
        f = open(cache_file, 'w')
        f.write(data)
        f.close()
        return data
    except:
        pass

    return None


def get_classpaths(view):
    classpaths = []

    complete = HaxeComplete_inst()
    build = complete.get_build(view)
    classpaths.extend(complete.__class__.stdPaths)

    for cp in build.classpaths:
        classpaths.append(os.path.join(build.cwd, cp))

    for lib in build.libs:
        if lib is not None:
            classpaths.append(lib.path)

    return classpaths


def get_env(copy_os_env=False):
    env = {}
    env["PATH"] = os.environ["PATH"]

    if copy_os_env:
        env = os.environ.copy()

    view = sublime.active_window().active_view()

    if view is not None :
        settings = view.settings()

        user_env = settings.get('build_env')
        if user_env:
            env.update(user_env)

        if settings.has("haxe_library_path"):
            env["HAXE_LIBRARY_PATH"] = settings.get(
                "haxe_library_path", ".")
            env["HAXE_STD_PATH"] = settings.get(
                "haxe_library_path", ".")

        if settings.has("haxe_path"):
            env["HAXE_PATH"] = settings.get(
                "haxe_path", "haxe")
            env["PATH"] += os.pathsep + os.path.dirname(
                settings.get("haxe_path"))

        if settings.has("haxelib_path"):
            env["PATH"] += os.pathsep + os.path.dirname(
                settings.get("haxelib_path"))

    return env


def parse_sig(sig):
    params = []
    spl = sig.split(" -> ")
    pars = 0;
    currentType = [];

    for t in spl :
        currentType.append( t )
        for ch in t:
            if ch in "({<" :
                pars += 1
            if ch in ")}>" :
                pars -= 1

        if pars == 0 :
            params.append(
                " -> ".join(currentType).replace('(', '').replace(')', ''))
            currentType = []

    ret = 'haxe-sublime-bundle-bug'
    if params:
        ret = params.pop()

    if not params:
        params = None
    elif len(params) == 1 and params[0] == "Void" :
        params = []

    return params, ret


def runcmd( args, input=None ):
    merged_env = get_env(True)

    try:
        if int(sublime.version()) >= 3000 :
            p = Popen(args, env=merged_env, stdout=PIPE, stderr=PIPE, stdin=PIPE, startupinfo=STARTUP_INFO)
        else:
            p = Popen([a.encode(sys.getfilesystemencoding()) for a in args], env=merged_env, stdout=PIPE, stderr=PIPE, stdin=PIPE, startupinfo=STARTUP_INFO)
        if isinstance(input, unicode) :
            input = input.encode('utf-8')
        out, err = p.communicate(input=input)
        return (out.decode('utf-8') if out else '', err.decode('utf-8') if err else '')
    except (OSError, ValueError) as e:
        err = u'Error while running %s: %s' % (args[0], e)
        if int(sublime.version()) >= 3000 :
            return ("",err)
        else:
            return ("", err.decode('utf-8'))

def show_quick_panel(_window, options, done, flags=0, sel_index=0):
    sublime.set_timeout(lambda: _window.show_quick_panel(options, done, flags, sel_index), 10)



class runcmd_async(object):
    """
    Enables to run subprocess commands in a different thread with TIMEOUT option.

    Based on jcollado's solution:
    http://stackoverflow.com/questions/1191374/subprocess-with-timeout/4825933#4825933
    """
    command = None
    process = None
    status = None
    output, error = '', ''

    def __init__(self, command):
        if isinstance(command, str):
            command = shlex.split(command)
        self.command = command

    def run(self, timeout=None, **kwargs):
        """ Run a command then return: (status, output, error). """
        def target(**kwargs):
            try:
                self.process = subprocess.Popen(self.command, **kwargs)
                self.output, self.error = self.process.communicate()
                self.status = self.process.returncode
            except:
                self.error = traceback.format_exc()
                self.status = -1
        # default stdout and stderr
        if 'stdout' not in kwargs:
            kwargs['stdout'] = subprocess.PIPE
        if 'stderr' not in kwargs:
            kwargs['stderr'] = subprocess.PIPE
        # thread
        thread = threading.Thread(target=target, kwargs=kwargs)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()
        return self.status, self.output, self.error

