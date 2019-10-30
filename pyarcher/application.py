# -*- coding: utf-8 -*-

"""User module."""
from pyarcher.base import ArcherBase
from pyarcher.field import Field


class Application(ArcherBase):
    """[summary].

    Args:
        Archer ([type]): [description]

    Returns:
        [type]: [description]

    """

    _metadata: dict = None
    _fields: list = None

    def __init__(self, app_id: int = None, **kwargs):
        self.app_id = app_id
        super().__init__(**kwargs)

    def _pass_archer_base(self):
        to_pass = [
            "url", "instance_name", "user_domain", "username", "password",
            "client_cert", "session_token"
        ]
        to_pass_dict = {
            key: value
            for key, value in self.__dict__.items()
            if key in to_pass and value
        }
        return to_pass_dict

    def refresh_app_details(self):
        api_url = f"core/system/user/{self.user_id}"
        resp_data = self.request_helper(api_url, method="get").json()
        self._metadata = resp_data['RequestedObject']
        return self._metadata

    def refresh_app_fields(self):
        api_url = f"core/system/fielddefinition/application/{self.app_id}"
        resp_data = self.request_helper(api_url, method="get").json()
        self._fields = [
            self.field(field['RequestedObject']['Id']) for field in resp_data
        ]
        return self._fields

    def _set_metadata(self, data: dict) -> dict:
        self._metadata = data
        return self._metadata

    @property
    def metadata(self):
        """Property method for metadata"""
        if not self._metadata:
            self._metadata = self.refresh_app_details()
        return self._metadata

    @property
    def fields(self):
        """Property method for metadata"""
        if not self._fields:
            self._fields = self.refresh_app_fields()
        return self._fields

    def field(self, field_id):
        to_pass = self._pass_archer_base()
        to_pass['field_id'] = field_id
        field = Field(**to_pass)
        return field
