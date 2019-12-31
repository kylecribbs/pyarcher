# -*- coding: utf-8 -*-

"""User module."""
from typing import TypeVar

from pyarcher.base import ArcherBase
from pyarcher.archer_types import GroupClass, UserClass

class User(ArcherBase):
    """[summary].

    Args:
        Archer ([type]): [description]

    Returns:
        [type]: [description]

    """

    _metadata: dict = None
    _groups: list = None

    def __init__(self, obj_id: int, **kwargs):
        self.obj_id = obj_id
        super().__init__(**kwargs)

    def refresh_metadata(self):
        api_url = f"core/system/user/{self.obj_id}"
        resp_data = self.request_helper(api_url, method="get").json()
        self._metadata = resp_data['RequestedObject']
        return self._metadata

    def refresh_groups(self):
        if self._groups:
            self._groups = self.archer.get_groups_by_user(self.obj_id)

    def get_user_email(self):
        resp = self.request_helper(
            f"core/system/usercontact/{self.obj_id}",
            method="get"
        )
        resp_data = resp.json()
        if resp_data[0]['IsSuccessful']:
            return resp_data

    def assign_role(self, role_id):
        """
        :param role_id: internal system id
        :return: log message of success oe failure
        """
        data = {
            "UserId": f"{self.obj_id}",
            "RoleId": f"{role_id}",
            "IsAdd": "true"
        }
        resp = self.request_helper(
            "core/system/userrole",
            method="put",
            data=data
        )
        return resp

    def remove_role(self, role_id):
        self.refresh_groups()
        pass

    def assign_group(self, group_id):
        """
        :param group: Name of the group how you see it in Archer
        :return: log message of success oe failure
        """
        data = {
            "UserId": f"{self.obj_id}",
            "GroupId": f"{group_id}",
            "IsAdd": "true"
        }
        resp = self.request_helper(
            "core/system/usergroup",
            method="put",
            data=data
        )
        self.refresh_groups()
        return resp

    def remove_group(self, group_id):
        pass

    @property
    def groups(self):
        if not self._groups:
            self._groups = self.archer.get_groups_by_user(self.obj_id)
        return self._groups

    @property
    def archer(self):
        archer = self.resource("archer")
        return archer

    def activate(self):
        """
        :return: log message of success or failure
        """
        resp = self.request_helper(
            f"core/system/user/status/active/{self.obj_id}",
            method="post"
        )
        return resp

    def deactivate(self):
        """
        :return: log message of success or failure
        """
        resp = self.request_helper(
            f"core/system/user/status/inactive/{self.obj_id}",
            method="post"
        )
        return resp
