# -*- coding: utf-8 -*-

"""User module."""
from pyarcher.base import ArcherBase


class ValuesList(ArcherBase):
    """[summary].

    Args:
        Archer ([type]): [description]

    Returns:
        [type]: [description]

    """

    _metadata: dict = None
    _values: list = None

    def __init__(self, values_list_id: int = None, **kwargs):
        self.values_list_id = values_list_id
        super().__init__(**kwargs)

    def refresh_values(self):
        api_url = "core/system/valueslistvalue/flat/valueslist/{}".format(
            self.values_list_id
        )
        resp_data = self.request_helper(api_url, method="get").json()
        self._values = [value['RequestedObject'] for value in resp_data]
        return self._values

    @property
    def values(self):
        """Property method for metadata"""
        if not self._values:
            self._values = self.refresh_values()
        return self._values

    @property
    def active_values(self):
        """Property method for metadata"""
        return [value for value in self.values if value['IsActive']]

    @property
    def inactive_values(self):
        """Property method for metadata"""
        return [value for value in self.values if not value['IsActive']]

    def add_value(self):
        # TODO: Create add value
        pass

    def remove_value(self):
        # TODO: Create remove value
        pass