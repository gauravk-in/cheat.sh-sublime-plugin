import sublime
import sublime_plugin
import requests
import os
import re

extension_language_dict = {
    ".py" : "python",
    ".cpp" : "cpp",
    ".hpp" : "cpp",
    ".c" : "c",
    ".h" : "cpp",
    ".sh" : "bash",
    ".css" : "css",
    ".html" : "html",
    ".htm" : "html",
    ".xhtml" : "html",
    ".jhtml" : "html",
    ".jsp" : "java",
    ".jspx" : "java",
    ".wss" : "java",
    ".do" : "java",
    ".action" : "java",
    ".js" : "javascript",
    ".pl" : "perl",
    ".php" : "php",
    ".php4" : "php",
    ".php3" : "php",
    ".phtml" : "php",
    ".rb" : "ruby",
    ".swift" : "swift",
}

syntaxFile_language_dict = {"Packages/Python/Python.sublime-syntax": "python"}

def getAnswer(language, query, recommendationNum = 0, withComments = True):
    recommendationStr = ""
    if (recommendationNum > 0):
        recommendationStr = '/' + str(recommendationNum)
    commentsStr = ""
    if withComments == False:
        commentsStr = "?Q"
    requestStr = 'http://cht.sh/' + language  + '/' + query + recommendationStr + commentsStr + '?T'
    return requests.get(requestStr).text

class CheatSheetUtils:
    def error_programming_language_unknown(self):
        sublime.message_dialog("Cheat.sh plugin could not deduce the programming language.\n\nPlease save the file with an appropriate extension or set the syntax from the Command Palette (Cmd + Shift + p) and typing \"Set Syntax:\"")

    def error_unsupported_programming_language(self):
        sublime.message_dialog("Cheat.sh plugin does not seem to support this programming language.\n\nPlease contact the developer at gaurav@gauravk.in to include support for this programming language.")
        
    def getProgrammingLanguage(self):
        fname = self.view.file_name()
        if fname is not None:
            filename, fileext = os.path.splitext(self.view.file_name());
            if fileext in extension_language_dict:
                return extension_language_dict[fileext]
            else:
                self.error_unsupported_programming_language()
                return 
        else:
            syntaxFile = self.view.settings().get('syntax')
            if syntaxFile in syntaxFile_language_dict:
                return syntaxFile_language_dict[syntaxFile]
            else:
                if syntaxFile == 'Packages/Text/Plain text.tmLanguage':
                    self.error_programming_language_unknown()
                else:
                    self.error_unsupported_programming_language()
                return None

class CheatSheetCommand(sublime_plugin.TextCommand, CheatSheetUtils):
    def run(self, edit):
        language = self.getProgrammingLanguage()
        if language is not None:
            for region in self.view.sel():
                if not region.empty():
                    s = self.view.substr(region)
                    s = re.sub(r'\s+(?!\n)', r'+', s)
                    self.view.replace(edit, region, getAnswer(language, s))

class CheatSheetMultipleSuggestionsCommand(sublime_plugin.TextCommand, CheatSheetUtils):
    def on_done(self, user_input):
        language = self.getProgrammingLanguage()
        if language is not None:
            newView = self.view.window().new_file()
            newView.settings().set('auto_indent', False)
            newView.settings().set('word_wrap', False)
            newView.set_syntax_file(self.view.settings().get('syntax'))
            sublime.active_window().focus_view(newView)
            separator = '\n\n' + "-"*80 + '\n' + "-"*80 + '\n' + "-"*80 + '\n\n'
            if sublime.active_window().active_view() == newView:
                newView.run_command('insert', {"characters": getAnswer(language, user_input)})
                newView.run_command('insert', {"characters": separator})
                newView.run_command('insert', {"characters": getAnswer(language, user_input, 1)})
                newView.run_command('insert', {"characters": separator})
                newView.run_command('insert', {"characters": getAnswer(language, user_input, 2)})

    def run(self, edit):
        self.view.window().show_input_panel("Cheat.sh", "", self.on_done, None, None)

class CheatSheetInputPanelCommand(sublime_plugin.TextCommand, CheatSheetUtils):
    def on_done(self, user_input):
        language = self.getProgrammingLanguage()
        if language is not None:
            old_auto_indent_status = self.view.settings().get('auto_indent')
            if (old_auto_indent_status == True):
                self.view.settings().set('auto_indent', False)
            self.view.run_command('insert', {"characters": getAnswer(language, user_input)})
            if (old_auto_indent_status == True):
                self.view.settings().set('auto_indent', True)

    def run(self, edit):
        self.view.window().show_input_panel("Cheat.sh", "", self.on_done, None, None)
        


