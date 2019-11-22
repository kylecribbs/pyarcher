# -*- coding: utf-8 -*-

"""User module."""
from pyarcher.base import ArcherBase


class User(ArcherBase):
    """[summary].

    Args:
        Archer ([type]): [description]

    Returns:
        [type]: [description]

    """

    _metadata: dict = None

    def __init__(self, user_id: int = None, **kwargs):
        self.user_id = user_id
        super().__init__(**kwargs)

    def refresh_user_details(self):
        api_url = f"core/system/user/{self.user_id}"
        resp_data = self.request_helper(api_url, method="get").json()
        self._metadata = resp_data['RequestedObject']
        return self._metadata

    def get_user_email(self):
        resp = self.request_helper(
            f"core/system/usercontact/{self.user_id}",
            method="get"
        )
        resp_data = resp.json()
        if resp_data[0]['IsSuccessful']:
            return resp_data

    def metadata(self, data: dict) -> dict:
        self._metadata = data
        return self._metadata

    @property
    def metadata(self):
        """Property method for metadata"""
        if not self._metadata:
            self._metadata = self.refresh_user_details()
        return self._metadata

    def assign_role(self, role_id):
        """
        :param role_id: internal system id
        :return: log message of success oe failure
        """
        data = {
            "UserId": f"{self.user_id}",
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
        pass

    def assign_group(self, group_id):
        """
        :param group: Name of the group how you see it in Archer
        :return: log message of success oe failure
        """
        data = {
            "UserId": f"{self.user_id}",
            "GroupId": f"{group_id}",
            "IsAdd": "true"
        }
        resp = self.request_helper(
            "core/system/usergroup",
            method="put",
            data=data
        )
        return resp

    def remove_group(self, group_id):
        pass

    def activate(self):
        """
        :return: log message of success or failure
        """
        resp = self.request_helper(
            f"core/system/user/status/active/{self.user_id}",
            method="post"
        )
        return resp

    def deactivate(self):
        """
        :return: log message of success or failure
        """
        resp = self.request_helper(
            f"core/system/user/status/inactive/{self.user_id}",
            method="post"
        )
        return resp
