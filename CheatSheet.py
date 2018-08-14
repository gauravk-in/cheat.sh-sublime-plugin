import sublime
import sublime_plugin
import requests
import os
import re

syntaxFile_language_dict = {"Packages/Python/Python.sublime-syntax": "python"}

def getAnswer(language, query, recommendationNum = 0, withComments = True):
    query = re.sub(r"\s+", "+", query)
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
        sublime.message_dialog("Cheat.sh plugin could not deduce the programming language.\n\nPlease save the file with an appropriate extension or set the syntax from the Command Palette by pressing Cmd + Shift + p and typing \"Set Syntax:\"")

    def error_unsupported_programming_language(self):
        sublime.message_dialog("Cheat.sh plugin does not seem to support this programming language.\n\nPlease contact the developer at gaurav@gauravk.in to include support for this programming language.")

    def getLanguage(self):
        syntaxFile = self.view.settings().get('syntax') 
        m = re.search('Packages/\w*/(?P<language>\w*)\.sublime-syntax', syntaxFile)
        if m:
            language = m.group("language")
            return "sublime:" + language.lower()
        else:
            fname = self.view.file_name()
            if fname is None:
                self.error_programming_language_unknown()
            m = re.search('/?(?!\w*/)*\w*\.(?P<fileext>\w*)$', fname)
            if m:
                fileext = m.group("fileext")
                return fileext.lower()
            else:
                self.error_programming_language_unknown()

class CheatSheetCommand(sublime_plugin.TextCommand, CheatSheetUtils):
    def run(self, edit, with_comments):
        language = self.getLanguage()
        if language is not None:
            for region in self.view.sel():
                if not region.empty():
                    query = self.view.substr(region)
                    self.view.replace(edit, region, getAnswer(language, query, 0, with_comments))
                    self.view.run_command("reindent")

class CheatSheetMultipleSuggestionsCommand(sublime_plugin.TextCommand, CheatSheetUtils):
    show_result_with_comments = True

    def on_done(self, user_input):
        language = self.getLanguage()
        if language is not None:
            newView = self.view.window().new_file()
            newView.settings().set('auto_indent', False)
            newView.settings().set('word_wrap', False)
            newView.set_syntax_file(self.view.settings().get('syntax'))
            sublime.active_window().focus_view(newView)
            separator = '\n\n' + "-"*80 + '\n' + "-"*80 + '\n' + "-"*80 + '\n\n'
            if sublime.active_window().active_view() == newView:
                newView.run_command('insert', {"characters": getAnswer(language, user_input, 0, self.show_result_with_comments)})
                newView.run_command('insert', {"characters": separator})
                newView.run_command('insert', {"characters": getAnswer(language, user_input, 1, self.show_result_with_comments)})
                newView.run_command('insert', {"characters": separator})
                newView.run_command('insert', {"characters": getAnswer(language, user_input, 2, self.show_result_with_comments)})

    def run(self, edit, with_comments):
        self.show_result_with_comments = with_comments
        input_panel_prompt = "Cheat.sh"
        if with_comments:
            input_panel_prompt = input_panel_prompt + " (with comments) :"
        else:
            input_panel_prompt = input_panel_prompt + " (without comments) :"
        self.view.window().show_input_panel(input_panel_prompt, "", self.on_done, None, None)

class CheatSheetInputPanelCommand(sublime_plugin.TextCommand, CheatSheetUtils):
    show_result_with_comments = True

    def on_done(self, user_input):
        language = self.getLanguage()
        if language is not None:
            old_auto_indent_status = self.view.settings().get('auto_indent')
            if (old_auto_indent_status == True):
                self.view.settings().set('auto_indent', False)
            self.view.run_command('insert', {"characters": getAnswer(language, user_input, 0, self.show_result_with_comments)})
            if (old_auto_indent_status == True):
                self.view.settings().set('auto_indent', True)

    def run(self, edit, with_comments):
        self.show_result_with_comments = with_comments
        input_panel_prompt = "Cheat.sh"
        if with_comments:
            input_panel_prompt = input_panel_prompt + " (with comments) :"
        else:
            input_panel_prompt = input_panel_prompt + " (without comments) :"
        self.view.window().show_input_panel(input_panel_prompt, "", self.on_done, None, None)