# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QFileDialog


class change_notes_path:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):
        notes_path = QFileDialog.getExistingDirectory(None, "Select Direcory", data['functions'].config('Notes path'))

        if notes_path:
            data['functions'].config('Notes path', notes_path)
            data['note_treeview'].set_current_dir(notes_path)
            #self.note_treeview.setRootIndex(self.file_model.index(self.config('Notes path')))
