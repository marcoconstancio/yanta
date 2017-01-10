# -*- coding: utf-8 -*-
import os
import string

from formlayout import fedit


class insert_table:
    def __init__(self):
        pass

    @staticmethod
    def load_process(data, args):
        action_path = os.path.dirname(__file__)
        libs_path = data['functions'].config('Libs path')
        style_class_name = "yanta_table_style"

        data['note_viewer'].call_function('apply_stylefile', os.path.join(action_path, 'table_insert_style.css'), style_class_name)
        data['note_viewer'].call_function('execute_jsfile', os.path.join(data['functions'].config('Libs path'), 'javacript', 'yanta', 'html_utils.js'))
        data['note_viewer'].call_function('execute_jsfile', os.path.join(action_path, 'insert_table_loadprocess.js'))

    @staticmethod
    def process(data, args):
        if args is None:
            #OPTIONS WINDOWS
            datagroup = [(None, '<b>Tables</b><br>Minimum Size: 1 Column x 2 Lines'),
                         ('Columns', 2),
                         ('Lines', 2),
                         ('Include Headers', True),
                         ('Width',[0,'0%', '5%', '10%', '15%', '20%', '25%', '30%', '35%', '40%', '45%', '50%', '55%', '60%',
                           '65%', '70%', '75%', '80%', '85%', '90%', '95%', '100%']),
                         ]
            table_html = ''

            result = fedit(datagroup, 'Table options')

            #GENERATE A TABLE IN HTML
            if result != None and result[0] > 0 and result[1] > 0:
                width = str(result[3]*5)
                table_html = '\\n<table width=\''+width+'%\'>\\n'
                if result[2]:
                    table_html += '<tr>'

                    for column in range(0, result[0]):
                        table_html += '<th>&nbsp;</th>'

                    table_html += '</tr>\\n'

                for line in range(0, result[1]):
                    table_html += '<tr>'

                    for column in range(0, result[0]):
                        table_html += '<td>&nbsp;</td>'

                    table_html += '</tr>\\n'
                table_html += '</table>\\n'

            #INSERT TABLE
            data['note_viewer'].call_function('insert_html',table_html)

        elif 'submenu_selected_option' in args:
            # Get safe filename from the name of the selected option
            valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
            filename = ''.join(c for c in args['submenu_selected_option'] if c in valid_chars)
            filename = filename.replace(' ', '_')  # I don't like spaces in filenames.

            # Run the javascript from the name
            data['note_viewer'].call_function('execute_jsfile', os.path.join(os.path.dirname(__file__), filename + '.js'))


