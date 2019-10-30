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

    def __init__(self, field_id: int = None, **kwargs):
        self.field_id = field_id
        super().__init__(**kwargs)

    def refresh_field_details(self):
        # TODO: Find Route
        api_url = f"core/system/user/{self.field_id}"
        resp_data = self.request_helper(api_url, method="get").json()
        self._metadata = resp_data['RequestedObject']
        return self._metadata

    def _set_metadata(self, data: dict) -> dict:
        self._metadata = data
        return self._metadata

    @property
    def metadata(self):
        """Property method for metadata"""
        if not self._metadata:
            self._metadata = self.refresh_field_details()
        return self._metadata
