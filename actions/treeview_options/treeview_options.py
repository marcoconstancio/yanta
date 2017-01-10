# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit

class treeview_options:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):
        if "submenu_selected_option" in args:
            #  data['note_treeview'].
            if args["submenu_selected_option"] == "Show Filetree Sizes":
                data['functions'].config('Show Filetree Sizes',not data['functions'].config('Show Filetree Sizes'), 'view')
            elif args["submenu_selected_option"] == "Show Filetree Types":
                data['functions'].config('Show Filetree Types',not data['functions'].config('Show Filetree Types'), 'view')
            elif args["submenu_selected_option"] == "Show Filetree Dates":
                data['functions'].config('Show Filetree Dates',not data['functions'].config('Show Filetree Dates'), 'view')

            data['functions'].save_configfile(data['functions'].config())
            data['note_treeview'].setColumnHidden(1, not data['functions'].config('Show Filetree Sizes', None, 'view'))
            data['note_treeview'].setColumnHidden(2, not data['functions'].config('Show Filetree Types', None, 'view'))
            data['note_treeview'].setColumnHidden(3, not data['functions'].config('Show Filetree Dates', None, 'view'))

    @staticmethod
    def get_data(data, args):
        if 'action' in args and 'value_name' in args and args['action'] == 'get_value' :
            return bool(data['functions'].config(args['value_name'], None, 'view'))

