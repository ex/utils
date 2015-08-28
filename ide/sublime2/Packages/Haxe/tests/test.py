import sublime, os, time
from functools import partial
from unittest import TestCase

version = sublime.version()

if version >= "3000":
    from UnitTesting.unittesting import DeferrableTestCase
else:
    from unittesting import DeferrableTestCase

# path to the Haxe package folder
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

class TestHxml(DeferrableTestCase):
    def setUp(self):
        self.window = sublime.active_window()
        if version >= "3000":
            self.ori_project_data = self.window.project_data()

    def tearDown(self):
        if version >= "3000":
            # restore the original project data
            self.window.set_project_data(self.ori_project_data)

        # show the test result
        self.window.open_file(os.path.join(root_path, "tests", "result.txt"))

    def set_project_folder(self, path):
        folders = [{
            "follow_symlinks": True,
            "path": path
        }]
        project_data = self.window.project_data()
        if project_data:
            project_data["folders"] = folders
        else:
            project_data = {
                "folders": folders
            }
        self.window.set_project_data(project_data)

    def assertTrueWait(self, expect, timeout_sec = 5):
        t = time.clock()
        while time.clock() - t < timeout_sec and not expect():
            yield
        self.assertTrue(expect())

    def test_hxml_simple(self):
        hxml_simple_path = os.path.join(root_path, "tests", "projects", "hxml_simple")
        self.set_project_folder(hxml_simple_path)
        view = self.window.open_file(os.path.join(hxml_simple_path, "Main.hx"))

        # syntax should be Haxe
        self.assertTrue("Haxe" in view.settings().get('syntax'))

        output_path = os.path.join(hxml_simple_path, "Main.n")
        if os.path.exists(output_path):
            os.remove(output_path)

        # test build (Command+B and Ctrl+Enter)
        expect = partial(os.path.exists, output_path)
        for cmd in ["build", "haxe_run_build", "haxe_save_all_and_build"]:
            self.window.run_command(cmd)
            for _ in self.assertTrueWait(expect):
                yield
            os.remove(output_path)

        # clean up
        self.window.focus_view(view)
        self.window.run_command("close_file")