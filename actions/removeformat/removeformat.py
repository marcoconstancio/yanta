# -*- coding: utf-8 -*-

class removeformat:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):
        data['note_viewer'].call_function('remove_format')