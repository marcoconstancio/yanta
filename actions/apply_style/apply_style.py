# -*- coding: utf-8 -*-
import os, sys, re, datetime

from PyQt5.QtWidgets import QMessageBox
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "libs", "python")))
from formlayout import fedit


class apply_style:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):
        style_class_name = "yanta_main_style"

        available_styles = [data['functions'].config('Default Color Style', None, 'view')]
        # available_styles += [('nostyle','No Style')]
        available_styles += data['functions'].get_styles()

        defs = [(None, '<b>Note Editor</b>'),
                ('Color Style', available_styles)]

        result = fedit(defs, "Select Style")


        if result:
            if not result[0]:
                style_file_content = "  "
            else:
                file_path = os.path.join(data['functions'].config('Plugins path'), 'styles', result[0])
                style_file_content = data['functions'].open_file(file_path)

                style_file_content = style_file_content.replace("\"","'").replace("\n"," ")
        else:
            style_file_content = ""

        data['note_viewer'].call_function('apply_style',style_file_content,style_class_name)

        # Runs available actions load_function method in other to prepare
        # the program/editor/... for those action
        editor_load_functions = data['functions'].session('editor_load_functions')

        if editor_load_functions:
            for (i, func_name) in enumerate(editor_load_functions):
                func = editor_load_functions[func_name]
                if 'load_process_function' in func:
                    func['load_process_function'](func['app_data'],func['custom_options'])
