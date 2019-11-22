# -*- coding: utf-8 -*-

"""User module."""
from pyarcher.base import ArcherBase


class Field(ArcherBase):
    """[summary].

    Args:
        Archer ([type]): [description]

    Returns:
        [type]: [description]

    """

    _metadata: dict = None
    _is_sub_form: bool = None
    _is_values_list: bool = None

    def __init__(self, obj_id: int = None, **kwargs):
        self.obj_id = obj_id
        super().__init__(**kwargs)

    def refresh_metadata(self):
        # TODO: Find Route
        api_url = f"core/system/user/{self.obj_id}"
        resp_data = self.request_helper(api_url, method="get").json()
        self._metadata = resp_data['RequestedObject']
        return self._metadata
