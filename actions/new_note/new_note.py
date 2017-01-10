# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit
from formlayout import fedit
import os
import time

class new_note:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):

        open_extensions = {}
        if data:
            if len(data['functions'].get_save_extensions()) > 0:
                open_extensions = data['functions'].get_save_extensions()

        viewers = data['functions'].get_viewers()
        note_description_default = "Rich text note"
        #note_description_default = "Simple text notes"

        note_descriptions = []
        note_extensions = []

        for viewer_name in viewers:
            note_descriptions.append((viewer_name, viewers[viewer_name]['note_description']))

            if note_description_default is None:
                note_description_default = viewers[viewer_name]['note_description']

            for extension in viewers[viewer_name]['open_extensions']:
                note_extensions.append(extension)

        note_descriptions.insert(0, note_description_default)

        # OPTIONS WINDOWS
        datagroup = [('Type', note_descriptions),
                     ('Name', 'note_' + time.strftime("%Y%m%d") + "_"+ time.strftime("%H%M"))]

        result = fedit(datagroup, 'Table options')

        if result:
            file_name = result[1]
            file_extension = viewers[result[0]]['open_extensions'][0]
            current_dir = data['note_treeview'].get_selected_path()

            if current_dir is None:
                current_dir = data['functions'].config('Notes path')

            file_name = data['functions'].new_file(current_dir, file_name + '.' + file_extension)

            # Set current selected index on side panel
            data['note_treeview'].set_selected_file(file_name)

            # Open conent
            data['note_viewer'].open_file(file_name, open_extensions[file_extension])
            data['note_viewer'].set_writeable()

            data['functions'].session('current_note', file_name)
            data['functions'].session('current_note_location', os.path.dirname(file_name) + os.path.sep)

            # Runs available actions load_function method in other to prepare
            # the program/editor/... for those action
            editor_load_functions = data['functions'].session('editor_load_functions')

            if editor_load_functions:
                for (i, func_name) in enumerate(editor_load_functions):
                    func = editor_load_functions[func_name]
                    if 'load_process_function' in func:
                        func['load_process_function'](func['app_data'], func['custom_options'])

            if data['functions'].config('Apply in new notes'):
                # print(data['functions'].call_function('apply_stylefile',config('Apply in all notes'))
                style_class_name = "yanta_main_style"
                file_path = os.path.join(data['functions'].config('Plugins path'), 'styles',
                                         data['functions'].config('Default Color Style'))

                data['note_viewer'].call_function('apply_stylefile', file_path, style_class_name)



