# -*- coding: utf-8 -*-

class blockquote:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):
        data['note_viewer'].call_function('block_quote')