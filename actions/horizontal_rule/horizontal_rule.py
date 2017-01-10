# -*- coding: utf-8 -*-

class horizontal_rule:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):
        data['note_viewer'].call_function('insert_horizontal_rule')