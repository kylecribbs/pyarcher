# -*- coding: utf-8 -*-

"""User module."""
from pyarcher.base import ArcherBase


class Record(ArcherBase):
    """[summary].

    Args:
        Archer ([type]): [description]

    Returns:
        [type]: [description]

    """
    _metadata: dict = None
    _values: list = None

    def __init__(self, application, obj_id: int = None, **kwargs):
        self.obj_id = obj_id
        super().__init__(**kwargs)
        self.application = application

    def refresh_metadata(self):
        api_url = f"core/content/fieldcontent/"
        fields = [field.metadata['Ids'] for field in self.application.feilds]
        data = {
            "FieldIds": fields,
            "ContentIds": self.obj_id
        }
        resp = self.request_helper(api_url, method="post", data=data)
        self._metadata = resp
        #self._metadata = resp_data['RequestedObject']
        return self._metadata
