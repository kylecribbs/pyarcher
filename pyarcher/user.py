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

    _metadata = None

    def __init__(self, user_id: int = None, **kwargs):
        self.user_id = user_id
        super().__init__(**kwargs)

    def get_user_details(self):
        """
        :param user_id: internal Archer user id
        :return: User object
        """
        api_url = f"core/system/user/{self.user_id}"
        resp_data = self.request_helper(api_url, method="get").json()
        return resp_data['RequestedObject']

    def get_user_email(self):
        resp = self.request_helper(
            f"core/system/usercontact/{self.user_id}",
            method="get"
        )
        resp_data = resp.json()
        if resp_data[0]['IsSuccessful']:
            return resp_data

    @property
    def metadata(self):
        """Property method for Email"""
        if not self._metadata:
            self._metadata = self.get_user_details()
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