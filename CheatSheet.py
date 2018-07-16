import sublime
import sublime_plugin
import requests
import os
import re

extension_language_dict = {".py" : "python",".cpp" : "cpp",".c" : "c",".sh" : "bash"}

class CheatSheetCommand(sublime_plugin.TextCommand):
    def print_save_file_error(self, edit):
        for region in self.view.sel():
            if not region.empty():
                s = self.view.substr(region)
                s = "!!! \n To use cheat.sh plugin, the file needs to be saved with an appopriate \n extension to indicate the programming language being used. (eg. .py, cpp etc) \n!!!"
                self.view.replace(edit, region, s)

    def print_unsupported_programming_language(self, edit, fileext):
        for region in self.view.sel():
            if not region.empty():
                s = self.view.substr(region)
                s = "!!! \n It seems that the programming language, as indicated by the extension \"" + fileext + "\" \n is not supported by cheat.sh plugin currently! Please contact the developer to include \n support for this programming langauge. \n!!!"
                self.view.replace(edit, region, s)

    def run(self, edit):
        fname = self.view.file_name()
        if fname == None:
            self.print_save_file_error(edit)
            return
        filename, fileext = os.path.splitext(self.view.file_name());
        if fileext in extension_language_dict:
            language = extension_language_dict[fileext]
        else:
            self.print_unsupported_programming_language(edit, fileext)
            return
        for region in self.view.sel():
            if not region.empty():
                s = self.view.substr(region)
                s = re.sub(r'\s+(?!\n)', r'+', s)
                r = requests.get('http://cht.sh/' + language  + '/' + s + '?T')
                s = r.text
                self.view.replace(edit, region, s)