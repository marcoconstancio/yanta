# -*- coding: utf-8 -*-
import os

from PyQt5.QtWidgets import QFileDialog


class open_note:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):

        open_extensions = {}
        if data:
            if len(data['functions'].get_save_extensions()) > 0:
                open_extensions = data['functions'].get_open_extensions()

        if args is None:
            args = {}

        if args is None or 'file_name' not in args:
            file_name = QFileDialog.getOpenFileName(None,
                                                    "Open note",
                                                    data['functions'].config('Notes path'),
                                                    "All Files (*." + " *.".join(open_extensions.keys()) + ")")

            args['file_name'] = file_name[0]

        if 'file_name' in args:
            if os.path.isfile(args['file_name']):
                file_name, file_extension = os.path.splitext(args['file_name'])
                file_extension = file_extension[1:]

                file_name = args['file_name']

                # Set current selected index on side panel
                data['note_treeview'].set_selected_file(file_name)

                # Open conent
                data['note_viewer'].open_file(file_name, open_extensions[file_extension])
                data['note_viewer'].set_writeable()

                data['functions'].session('current_note', file_name)
                data['functions'].session('current_note_location', os.path.dirname(file_name))# + os.path.sep)

                # Runs available actions load_function method in other to prepare
                # the program/editor/... for those action
                editor_load_functions = data['functions'].session('editor_load_functions')

                if editor_load_functions:
                    for (i, func_name) in enumerate(editor_load_functions):
                        func = editor_load_functions[func_name]
                        if 'load_process_function' in func:
                            func['load_process_function'](func['app_data'],func['custom_options'])

                if data['functions'].config('Apply in opened notes'):
                    #print(data['functions'].call_function('apply_stylefile',config('Apply in all notes'))
                    style_class_name = "yanta_main_style"
                    file_path = os.path.join(data['functions'].config('Plugins path'), 'styles', data['functions'].config('Default Color Style'))
                    data['note_viewer'].call_function('apply_stylefile', file_path, style_class_name)

