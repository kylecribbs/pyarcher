# -*- coding: utf-8 -*-

"""User module."""
from dataclasses import dataclass

from pyarcher.archer import Archer


@dataclass
class Group(Archer):
    """[summary].

    Args:
        Archer ([type]): [description]

    Returns:
        [type]: [description]

    """

    group_id: int
    _name: str = None
    _roles: list = None
    _members: list = None

    def __post_init__(self, *args, **kwargs):
        """Post Init"""
        super().__init__(*args, **kwargs)

    def get_group_details(self):
        """
        :param user_id: internal Archer user id
        :return: User object
        """
        api_url = f"core/system/group/{self.group_id}"
        resp_data = self.request_helper(api_url, method="get").json()
        # TODO: set self attributes from resp