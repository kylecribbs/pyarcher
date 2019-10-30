# -*- coding: utf-8 -*-

"""User module."""
from pyarcher.base import ArcherBase
from pyarcher.field import Field


class SubForm(ArcherBase):
    """[summary].

    Args:
        Archer ([type]): [description]

    Returns:
        [type]: [description]

    """

    _metadata: dict = None
    _fields: list = None

    def __init__(self, sub_form_id: int = None, **kwargs):
        self.sub_form_id = sub_form_id
        super().__init__(**kwargs)