# -*- coding: utf-8 -*-
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QFileDialog


class saveas_note:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):
        if args is None:
            args = {}
            file_name_filters = []

            # Todo add extension names
            if len(data['note_viewer'].get_save_extensions()) > 0:
                file_name_filters = data['note_viewer'].get_save_extensions()

            extension_list = []

            for ext in file_name_filters:
                extension_list.append(ext[:1].upper() + ext[1:] + " (*." + ext + ")")

            filename, format = QFileDialog.getSaveFileName(None,
                                                            "Save As Note",
                                                            data['functions'].config('Notes path'),
                                                            ";;".join(extension_list),
                                                            '',
                                                            QFileDialog.DontUseNativeDialog)

            if format:
                file = QFileInfo(filename)
                if not file.suffix():
                    first_ext = format[format.find("(") + 1:format.find(")")].split("*.")[1]
                    filename += '.' + first_ext

            if filename:
                data['functions'].save_file(filename, data['note_viewer'].get_content())



