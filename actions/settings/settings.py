# -*- coding: utf-8 -*-
import os, sys, datetime

from PyQt5.QtWidgets import QMessageBox

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "libs", "python")))
from formlayout import fedit


class settings:
    def __init__(self):
        self.this = self
        pass

    @staticmethod
    def process(data, args):
        save_extensions = []

        if len(data['functions'].get_save_extensions()) > 0:
            save_extensions = list(data['functions'].get_save_extensions().keys())

        general_tab = [(None, '<b>Paths</b>'),
                       ('Notes path','dir|' + data['functions'].config('Notes path')),
                       (None, '<b>Extensions</b>'),
                       ('Default extension', [data['functions'].config('Default extension')] + save_extensions)
                       ]
        view_tab = [(None, '<b>Note Editor</b>'),
                    ('Default Color Style', [data['functions'].config('Default Color Style', None, 'view')] + data['functions'].get_styles()),
                    ('Apply in new notes', data['functions'].config('Apply in new notes', None, 'view')),
                    ('Apply in opened notes', data['functions'].config('Apply in opened notes', None, 'view')),

                    (None, '<b>Filetree</b>'),
                    ('Show Filetree Sizes', data['functions'].config('Show Filetree Sizes')),
                    ('Show Filetree Types', data['functions'].config('Show Filetree Types')),
                    ('Show Filetree Dates', data['functions'].config('Show Filetree Dates'))
                    ]

        extensions_tab = [(None, '<b>Show Extensions</b>')]

        extensions_list = list(data['functions'].get_open_extensions().keys())

        show_extensions_list = data['functions'].config('Show Extensions')
        for ext in extensions_list:
            if ext in show_extensions_list:
                extensions_tab.append((ext, True))
            else:
                extensions_tab.append((ext,False))

        printer_tab = [('Color Mode', [data['functions'].config('Color Mode', None, 'printer'), ('0', 'Grayscale'), ('1', 'Color')]),
                       ('Orientation',
                        [data['functions'].config('Orientation', None, 'printer'), ('0', 'Portrait'), ('1', 'Landscape')]),
                       ('Paper Size',
                        [data['functions'].config('Paper Size', None, 'printer'), ('5', 'A0'), ('6', 'A1'), ('7', 'A2'), ('8', 'A3'),
                         ('0', 'A4'), ('9', 'A5'), ('10', 'A6'), ('11', 'A7'),
                         ('12', 'A8'), ('13', 'A9'),
                         ('14', 'B0'), ('15', 'B1'),
                         ('17', 'B2'), ('18', 'B3'), ('19', 'B4'), ('1', 'B5'),
                         ('20', 'B6'), ('21', 'B7'), ('22', 'B8'), ('23', 'B9'),
                         ('16', 'B10'),
                         ('24', 'C5E'), ('25', 'Comm10E'), ('26', 'DLE'),
                         ('4', 'Executive'), ('27', 'Folio'), ('28', 'Ledger'),
                         ('3', 'Legal'), ('2', 'Letter'), ('29', 'Tabloid'),
                         ('30', 'Custom')]),
                       ('Paper Unit',
                        [data['functions'].config('Paper Unit', None, 'printer'), ('0', 'Millimeter'), ('1', 'Point'), ('2', 'Inch'),
                         ('3', 'Pica'),
                         ('4', 'Didot'), ('5', 'Cicero'), ('6', 'DevicePixel')]),
                       ('Paper Margins', data['functions'].config('Paper Margins', None, 'printer')),
                       ('Dots Per Inch', data['functions'].config('Dots Per Inch', None, 'printer'))
                       ]

        all_defs = [(general_tab, "General", None),
                    (view_tab, "View", None),
                    (printer_tab, "Printer", None),
                    (extensions_tab, "Extensions", None)]

        extension_defs = data['functions'].get_extension_definitions()

        for e_defs in extension_defs:
            all_defs.append((e_defs['definitions'], e_defs['name'], None))


        result =  fedit(all_defs, "Settings")


        if result:
            selected_extensions = result.pop()
            selected_extensions_def = all_defs.pop()
            show_extensions_list = []

            for idx, val in enumerate(selected_extensions):
                if val:
                    show_extensions_list.append(extensions_list[idx])

            data['functions'].save_configfile(result, all_defs)
            data['functions'].config('Show Extensions',show_extensions_list)
            data['functions'].save_configfile()

            # APPLY SETTINGS
            data['note_treeview'].setColumnHidden(1, not data['functions'].config('Show Filetree Sizes', None, 'view'))
            data['note_treeview'].setColumnHidden(2, not data['functions'].config('Show Filetree Types', None, 'view'))
            data['note_treeview'].setColumnHidden(3, not data['functions'].config('Show Filetree Dates', None, 'view'))

            data['note_treeview'].set_current_dir(data['functions'].config('Notes path'))

            if data['functions'].config('Notes path') and data['functions'].config('Default Color Style', None, 'view'):
                data['note_viewer'].call_function('apply_stylefile',os.path.join(data['functions'].config('Plugins path'), 'styles', data['functions'].config('Default Color Style', None, 'view')))

            file_name_filters = ["*." + ext for ext in data['functions'].config('Show Extensions')]
            file_name_filters.append("*.randomext")

            data['note_treeview'].get_file_model().setNameFilters(file_name_filters)