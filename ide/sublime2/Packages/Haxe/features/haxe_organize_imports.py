from sublime import Region
from sublime_plugin import TextCommand
import re

try:  # Python 3
    from ..HaxeHelper import importLine, packageLine
except (ValueError):  # Python 2
    from HaxeHelper import importLine, packageLine


class HaxeOrganizeImports(TextCommand):

    def erase_line(self, edit, point):
        rgn = self.view.full_line(point)
        self.view.erase(edit, rgn)
        return rgn.end() - rgn.begin()

    def extract_imports(self, edit):
        src = self.get_view_src()
        indent = ""
        splitted_classes = []
        classes = []
        wildcards = {}
        import_pos = -1
        offset = 0
        cur_package = self.get_cur_package(src)

        for mo in importLine.finditer(src):
            if import_pos == -1:
                import_pos = mo.start(0)
                indent = mo.group(1)

            clazz = mo.group(2)
            packagepath, _, classname = clazz.rpartition(".")

            if packagepath != "" and packagepath != cur_package:
                splitted_classes.append((packagepath, classname))
            if classname == "*":
                wildcards[packagepath] = True

            offset += self.erase_line(edit, mo.start(0) - offset)

        while True:
            if not splitted_classes:
                break
            splitted_class = splitted_classes.pop()
            if splitted_class[1] == "*" or splitted_class[0] not in wildcards:
                classes.append(".".join(splitted_class))

        return classes, import_pos, indent

    def get_cur_package(self, src):
        mo = packageLine.search(src)
        return "" if mo is None else mo.group(1)

    def get_import_pos(self):
        src = self.get_view_src()
        mo = packageLine.search(src)
        pos = 0
        if mo is not None:
            pos = mo.end(0)

        return pos

    def get_view_src(self):
        return self.view.substr(Region(0, self.view.size()))

    def import_classes(self, edit, classes, pos, indent):
        ins = ''

        for clazz in classes:
            ins += "{}import {};\n".format(indent, clazz)

        self.view.insert(edit, pos, ins)

    def organize_classes(self, classes, sort):
        src = self.get_view_src()
        organized_classes = []

        for clazz in classes:
            if clazz in organized_classes:
                continue

            classname = clazz.rpartition(".")[2]
            if classname != "*":
                mo = re.search("\W{}\W".format(classname), src)
                if mo is None:
                    continue

            organized_classes.append(clazz)

        if sort:
            organized_classes.sort()
        return organized_classes

    def run(self, edit, new_import=None, sort=True):
        classes, import_pos, indent = self.extract_imports(edit)

        if new_import is not None:
            classes.append(new_import)
        if len(classes) == 0:
            return
        if import_pos == -1:
            import_pos = self.get_import_pos()

        classes = self.organize_classes(classes, sort)
        self.import_classes(edit, classes, import_pos, indent)
