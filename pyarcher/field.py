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

    def __init__(self, field_id: int = None, **kwargs):
        self.field_id = field_id
        super().__init__(**kwargs)

    def refresh_field_details(self):
        # TODO: Find Route
        api_url = f"core/system/user/{self.field_id}"
        resp_data = self.request_helper(api_url, method="get").json()
        self._metadata = resp_data['RequestedObject']
        return self._metadata

    def check_if_values_list(self):
        if self.metadata['Type'] == 4:
            return True
        return False

    def check_if_sub_form(self):
        if self.metadata['Type'] == 24:
            return True
        return False

    def _set_metadata(self, data: dict) -> dict:
        self._metadata = data
        return self._metadata

    @property
    def metadata(self):
        """Property method for metadata"""
        if not self._metadata:
            self._metadata = self.refresh_field_details()
        return self._metadata

    @property
    def is_sub_form(self):
        """Property method for is_sub_form"""
        if not self._is_sub_form:
            self._is_sub_form = self.check_if_sub_form()
        return self._is_sub_form

    @property
    def is_values_list(self):
        """Property method for is_values_list"""
        if not self._is_values_list:
            self._is_values_list = self.check_if_values_list()
        return self._is_values_list
