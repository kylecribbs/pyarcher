# -*- coding: utf-8 -*-

"""User module."""
from pyarcher.base import ArcherBase
from pyarcher.field import Field
from pyarcher.values_list import ValuesList


class Application(ArcherBase):
    """[summary].

    Args:
        Archer ([type]): [description]

    Returns:
        [type]: [description]

    """

    _metadata: dict = None
    _fields: list = None

    def __init__(self, obj_id: int = None, **kwargs):
        self.obj_id = obj_id
        super().__init__(**kwargs)

    def refresh_metadata(self):
        api_url = f"core/system/user/{self.obj_id}"
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
        # Prevents circular import
        from pyarcher.field_type_enum import FieldType

        api_url = f"core/system/fielddefinition/application/{self.obj_id}"
        resp_data = self.request_helper(api_url, method="get").json()
        self._fields = []
        for json_field in resp_data:
            try:
                field_type = FieldType(json_field['RequestedObject']['Type'])
            except ValueError:
                field_type = FieldType.OTHER

            field = self.field(json_field['RequestedObject']['Id'])
            field.metadata = json_field['RequestedObject']

            validated_field = self.resource(
                field_type.class_name,
                field.metadata[field_type.key]
            )

            self._fields.append(validated_field)

        return self._fields

    @property
    def fields(self):
        """Property method for metadata"""
        if not self._fields:
            self._fields = self.refresh_app_fields()
        return self._fields

    def field(self, obj_id):
        return self.resource("field", obj_id=obj_id)

    def values_list(self, obj_id):
        return self.resource("values_list", obj_id=obj_id)

    def records(self):
        pass