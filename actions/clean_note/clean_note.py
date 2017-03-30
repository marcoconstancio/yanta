# -*- coding: utf-8 -*-
import os, sys, re, datetime

from PyQt5.QtWidgets import QMessageBox
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "libs", "python")))
from formlayout import fedit


class clean_note:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):
        # style_class_name = "yanta_main_style"
        #
        # available_styles = [data['functions'].config('Default Color Style', None, 'view')]
        # # available_styles += [('nostyle','No Style')]
        # available_styles += data['functions'].get_styles()

        defs = [('All elements', True),
                ('Bold element', True),
                ('Code element', True),
                ('Div element', True),
                ('Headings', True),
                ('Images', True),
                ('Italic element', True),
                ('Lists', True),
                ('Paragraph', True),
                ('Preformated element', True),
                ('Span element', True),
                ('Tables', True)]

        result = fedit(((defs, "Style Tag", "Remove style html tag<br/> for selected elements"),), "Clean Note")

        if result:
            js = "var style_tag_selected_elements = {}; "
            for index, value in enumerate(result[0]):
                js += 'style_tag_selected_elements["'+str(defs[index][0])+'"] = ' + str(value).lower() + '; '

            data['note_viewer'].call_function('execute_js', js)
            data['note_viewer'].call_function('execute_jsfile', os.path.join(os.path.dirname(__file__), 'clean_note.js'))


        # Runs available actions load_function method in other to prepare
        # the program/editor/... for those action
        editor_load_functions = data['functions'].session('editor_load_functions')

        if editor_load_functions:
            for (i, func_name) in enumerate(editor_load_functions):
                func = editor_load_functions[func_name]
                if 'load_process_function' in func:
                    func['load_process_function'](func['app_data'],func['custom_options'])
