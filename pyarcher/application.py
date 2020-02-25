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
    _fields: dict = None

    def __init__(self, obj_id: int = None, **kwargs):
        """Application Init."""
        self.obj_id = obj_id
        super().__init__(**kwargs)

    def check_alias(self):
        """Check to see if Alias is a duplicate or exists."""
        correct_alias = [
            endpoint for endpoint in self.endpoints
            if self.metadata['Alias'] == endpoint['name']
        ]
        if correct_alias:
            self.logger.info("Found alias endpoint")
            return True
        self.logger.error("Unknown Alias")

    def refresh_metadata(self):
        api_url = f"core/system/application/{self.obj_id}"
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

        resp_data = self.raw_fields().json()
        self._fields = {}
        for json_field in resp_data:
            #break out into a method
            try:
                field_type = FieldType(json_field['RequestedObject']['Type'])
            except ValueError:
                field_type = FieldType.OTHER

            field = self.field(json_field['RequestedObject']['Id'])
            field.metadata = json_field['RequestedObject']
            validated_field = self.resource(
                field_type.class_name, obj_id=field.metadata[field_type.key])

            self._fields.update(
                {json_field['RequestedObject']['Alias']: validated_field})

        return self._fields

    @property
    def fields(self):
        """Property method for metadata"""
        if not self._fields:
            self._fields = self.refresh_app_fields()
        return self._fields

    def raw_fields(self):
        """Return Dictionary of all fields."""
        api_url = f"core/system/fielddefinition/application/{self.obj_id}"
        resp_data = self.request_helper(api_url, method="get")
        return resp_data

    def field(self, obj_id):
        # return field type (aka values list, etc)
        return self.resource("field", obj_id=obj_id)

    # def records(self):
    #     records = self.resource(
    #         "record",
    #         obj_id=field.metadata[field_type.key],
    #         application=self.obj_id
    #     )

    def content(self):
        """Generator for all content records."""
        skip = 0
        while True:
            data = self.raw_content(skip=skip).json()
            if len(data['value']) == 0:
                return
            skip += 1000
            yield data['value']

    def raw_content(self, skip=0):
        """Content records."""
        api_url = f"{self.metadata['Alias']}?skip={skip}"
        resp_data = self.request_helper(api_url,
                                        content_api=True,
                                        method="get")
        return resp_data

    def new_record(self, **kwargs):
        """Create a new record."""
