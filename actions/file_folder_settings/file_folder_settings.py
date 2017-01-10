# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit

class file_folder_settings:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):
        pass
        # # http://rra.etc.br/MyWorks/2009/08/07/pyqt-04-dialogos-com-qinputdialog/
        # filename, ok = QtWidgets.QInputDialog.getText(None, 'New Note',
        #                                               'Enter a name for the note with the desired extension.',
        #                                               QLineEdit.Normal,
        #                                               "Note_xpto." + data['functions'].get_extensions('default'))
        #
        # if ok:
        #     current_dir = data['note_treeview'].get_selected_path()
        #
        #     if current_dir is None:
        #         current_dir = data['functions'].config('Notes path')
        #
        #     file_name = data['functions'].new_note(current_dir, filename)
        #     # Set current selected index onm side panel
        #     data['note_treeview'].set_selected_file(file_name)
        #     # Set editing area content
        #     data['note_viewer'].set_html(data['functions'].open_note(file_name))
        #     data['note_viewer'].execute_js(data['functions'].get_javascript_plugins())