# -*- coding: utf-8 -*-

"""User module."""
from pyarcher.base import ArcherBase


class Group(ArcherBase):
    """[summary].

    Args:
        Archer ([type]): [description]

    Returns:
        [type]: [description]

    """

    group_id: int = None
    _metadata: dict = None

    def __init__(self, group_id: int, **kwargs):
        self.group_id = group_id
        super().__init__(**kwargs)

    def refresh_group_details(self):
        api_url = f"core/system/group/{self.group_id}"
        resp_data = self.request_helper(api_url, method="get").json()
        self._metadata = resp_data['RequestedObject']
        return self._metadata

    def metadata(self, data: dict) -> dict:
        self._metadata = data
        return self._metadata

    @property
    def metadata(self):
        """Property method for Email"""
        if not self._metadata:
            self._metadata = self.refresh_group_details()
        return self._metadata

    def add_user(self, user_id):
        pass

    def remove_user(self, user_id):
        pass

    def members(self):
        pass

    def member_of(self):
        pass