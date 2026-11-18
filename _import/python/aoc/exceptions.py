# -*- coding: utf-8 -*-


class NoSuchException(Exception):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        super().__init__(f'No such {key} {value}')
