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

    OTHER = (0, "field", 'Id')
    TEXT = (1, "field", "Id")
    NUMERIC = (2, "field", "Id")
    DATE = (3, "field", "Id")
    VALUES_LIST = (4, "values_list", "RelatedValuesListId")
    TRACKINGID = (6, "field", "Id")
    EXTERNAL_LINKS = (7, "field", "Id")
    USER_GROUP_LIST = (8, "field", "Id")
    CROSS_REFERENCE = (9, "field", "Id")
    ATTACHMENT = (11, "field", "Id")
    IMAGE = (12, "field", "Id")
    CROSS_APPLICATION_STATUS_TRACKING = (14, "field", "Id")
    MATRIX = (16, "field", "Id")
    IP_ADDRESS = (19, "field", "Id")
    RECORD_STATUS = (20, "field", "Id")
    FIRST_PUBLISHED = (21, "field", "Id")
    LAST_UPDATED = (22, "field", "Id")
    RELATED_RECORD = (23, "field", "Id")
    SUB_FORM = (24, "application", "RelatedSubformId")
    HISTORY_LOG = (25, "field", "Id")
    DISCUSSION = (26, "field", "Id")
    MULTIPLE_REFERENCE_DISPLAY_CONTROL = (27, "field", "Id")
    QUESTIONNAIRE_REFERENCE = (28, "field", "Id")
    ACCESS_HISTORY = (29, "field", "Id")
    VOTING = (30, "field", "Id")
    SCHEDULER = (31, "field", "Id")
    #CROSS_APPLICATION_STATUS_TRACKING_VALUE = (1001, "", "")
