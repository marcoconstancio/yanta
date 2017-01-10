# -*- coding: utf-8 -*-
import os
import os.path
import base64

class insert_checkbox:
    def __init__(self):
        pass

    @staticmethod
    def load_process(data, args):
        action_path = os.path.dirname(__file__)

        # UNCHECKED IMAGE FILE
        filepath_unchecked = os.path.join(action_path, 'check_box_unchecked.jpg')
        filename_unchecked, fileextension_unchecked = os.path.splitext(filepath_unchecked)
        fileextension_unchecked = fileextension_unchecked[1:]

        image_encoded_data_unchecked = base64.b64encode(open(filepath_unchecked, "rb").read())
        base64_image_unchecked = "data:image/" + fileextension_unchecked + ";base64," + image_encoded_data_unchecked.decode('ascii')

        # CHECKED IMAGE FILE
        filepath_checked = os.path.join(action_path, 'check_box_checked.jpg')
        filename_checked, fileextension_checked = os.path.splitext(filepath_checked)
        fileextension_checked = fileextension_checked[1:]

        image_encoded_data_checked = base64.b64encode(open(filepath_checked, "rb").read())
        base64_image_checked = "data:image/" + fileextension_checked + ";base64," + image_encoded_data_checked.decode('ascii')

        data['note_viewer'].call_function('execute_js', "var base64_image_checked = '" + base64_image_checked + "';")
        data['note_viewer'].call_function('execute_js', "var base64_image_unchecked = '" + base64_image_unchecked + "';")

        data['note_viewer'].call_function('execute_jsfile', os.path.join(data['functions'].config('Libs path'), 'javacript', 'yanta', 'html_utils.js'))
        data['note_viewer'].call_function('execute_jsfile', os.path.join(os.path.dirname(__file__), 'insert_checkbox_loadprocess.js'))


    @staticmethod
    def process(data, args):
        # UNCHECKED IMAGE FILE
        # filepath_unchecked = os.path.join(os.path.dirname(__file__), 'check_box_unchecked.jpg')
        # filename_unchecked, fileextension_unchecked = os.path.splitext(filepath_unchecked)
        # fileextension_unchecked = fileextension_unchecked[1:]
        #
        # image_encoded_data_unchecked = base64.b64encode(open(filepath_unchecked, "rb").read())
        # base64_image_unchecked = "data:image/" + fileextension_unchecked + ";base64," + image_encoded_data_unchecked.decode('ascii')
        #
        # # CHECKED IMAGE FILE
        # filepath_checked = os.path.join(os.path.dirname(__file__), 'check_box_checked.jpg')
        # filename_checked, fileextension_checked = os.path.splitext(filepath_checked)
        # fileextension_checked = fileextension_checked[1:]
        #
        # image_encoded_data_checked = base64.b64encode(open(filepath_checked, "rb").read())
        # base64_image_checked = "data:image/" + fileextension_checked + ";base64," + image_encoded_data_checked.decode('ascii')
        #
        # # SET THE BASE64 CHECKBOXES IMAGES
        # data['note_viewer'].call_function('execute_js', "var base64_image_unchecked = '" + base64_image_unchecked + "';")
        # data['note_viewer'].call_function('execute_js', "var base64_image_checked = '" + base64_image_checked + "';")

        # Run javascript file for adding/removing checkbox
        data['note_viewer'].call_function('execute_jsfile', os.path.join(data['functions'].config('Libs path'), 'javacript', 'yanta', 'html_utils.js'))
        data['note_viewer'].call_function('execute_jsfile', os.path.join(os.path.dirname(__file__), 'insert_checkbox.js'))

        #data['note_viewer'].execute_jsfile(os.path.join(os.path.dirname(__file__), 'insert_checkbox.js'))


