# -*- coding: utf-8 -*-

"""User module."""

from enum import Enum, unique


@unique
class FieldType(bytes, Enum):
    def __new__(cls, value, class_name, key):
        obj = bytes.__new__(cls, [value])
        obj._value_ = value
        obj.class_name = class_name
        obj.key = key
        return obj

    SUB_FORM = (24, "application", "RelatedSubformId")
    VALUES_LIST = (4, "values_list", "RelatedValuesListId")
    OTHER = (0, "field", 'Id')
