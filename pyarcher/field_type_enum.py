# -*- coding: utf-8 -*-

"""User module."""

from enum import Enum, unique

from pyarcher.values_list import ValuesList
from pyarcher.application import Application
from pyarcher.field import Field


@unique
class FieldType(bytes, Enum):
    def __new__(cls, value, inst_class, key):
        obj = bytes.__new__(cls, [value])
        obj._value_ = value
        obj.inst_class = inst_class
        obj.key = key
        return obj

    SUB_FORM = (24, Application, "RelatedSubformId")
    VALUES_LIST = (4, ValuesList, "RelatedValuesListId")
    OTHER = (0, Field, 'Id')
