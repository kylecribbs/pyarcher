# -*- coding: utf-8 -*-

"""User module."""
from pyarcher.base import ArcherBase
from pyarcher.field import Field
from pyarcher.values_list import ValuesList
from pyarcher.sub_form import SubForm


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

    def check_field_type(self, field: Field):
        if field.is_sub_form:
            pass

        if field.is_values_list:
            return self.values_list(field.metadata['RelatedValuesListId'])

        #return field

    def refresh_app_fields(self):
        api_url = f"core/system/fielddefinition/application/{self.app_id}"
        resp_data = self.request_helper(api_url, method="get").json()
        self._fields = []
        for field in resp_data:
            new_field = self.field(field['RequestedObject']['Id'])
            new_field._set_metadata(field['RequestedObject'])
            validated_field = self.check_field_type(new_field)

            self._fields.append(validated_field)

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

    def values_list(self, values_list_id):
        to_pass = self._pass_archer_base()
        to_pass['values_list_id'] = values_list_id
        values_list = ValuesList(**to_pass)
        return values_list
