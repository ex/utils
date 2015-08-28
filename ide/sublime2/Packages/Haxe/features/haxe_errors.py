import os
import re
import sublime
import traceback

errors = []
re_compiler_output = re.compile(
    "^(.+):(\\d+): (lines|characters?) (\\d+)(?:-(\\d+))? : (.*)$", re.M)


def extract_errors(str, cwd):
    global errors
    errors = []

    for infos in re_compiler_output.findall(str):
        infos = list(infos)
        # print(infos)
        f = infos.pop(0)

        if not os.path.isabs(f):
            f = os.path.join(cwd, f)
        f = os.path.normpath(f)

        l = int(infos.pop(0)) - 1

        metric = infos.pop(0)

        left = int(infos.pop(0))
        right = infos.pop(0)
        if right != "":
            right = int(right)
        else:
            right = left + 1

        m = infos.pop(0)

        if metric == "lines":
            left -= 1

        errors.append({
            "file": f,
            "line": l,
            "metric": metric,
            "from": left,
            "to": right,
            "message": m
        })

    # print(errors)
    if len(errors) > 0:
        sublime.status_message(errors[0]["message"])

    return errors


def highlight_errors(view, duration=0):
    global errors

    fn = view.file_name()
    line_regions = []
    char_regions = []

    if fn is None:
        return

    for e in errors:
        if e and \
                os.path.exists(e["file"]) and \
                os.path.exists(fn) and \
                os.stat(e["file"]) == os.stat(fn):
            metric = e["metric"]
            l = e["line"]
            left = e["from"]
            right = e["to"]

            if metric.startswith("character"):
                # retrieve character positions from utf-8 bytes offset reported
                # by compiler
                try:
                    line = view.substr(
                        view.line(view.text_point(l, 0))).encode("utf-8")
                    left = len(line[:left].decode("utf-8"))
                    right = len(line[:right].decode("utf-8"))

                    a = view.text_point(l, left)
                    b = view.text_point(l, right)
                    char_regions.append(sublime.Region(a, b))
                except:
                    print(traceback.print_exc())
            else:
                a = view.text_point(left, 0)
                b = view.text_point(right, 0)
                line_regions.append(sublime.Region(a, b))

            view.set_status("haxe-status", "Error: " + e["message"])

            if duration > 0:
                # show once
                e.clear()

    if duration > 0:
        sublime.set_timeout(
            lambda: highlight_errors(view), duration)

    gutter_style = view.settings().get('haxe_errors_gutter_style', 'dot')
    if gutter_style == 'none':
        gutter_style = ''

    draw_style = view.settings().get('haxe_errors_style', 'outline')
    if draw_style == 'outline':
        draw_style = sublime.DRAW_OUTLINED
    elif draw_style == 'fill':
        draw_style = 0
    else:
        draw_style = sublime.HIDDEN

    view.add_regions(
        "haxe-error-lines", line_regions, "invalid", gutter_style, draw_style)
    view.add_regions(
        "haxe-error", char_regions, "invalid", gutter_style, draw_style)
