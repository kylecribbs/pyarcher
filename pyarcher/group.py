# -*- coding: utf-8 -*-

"""User module."""
from typing import TypeVar

from pyarcher.base import ArcherBase
from pyarcher.archer_types import GroupClass, UserClass


class Group(ArcherBase):
    """[summary].

    Args:
        Archer ([type]): [description]

    Returns:
        [type]: [description]

    """

    group_id: int = None
    _metadata: dict = None
    _members = None
    _parent_groups = None
    _child_groups = None
    _all_members = None

    def __init__(self, obj_id: int, **kwargs):
        """Init."""
        self.obj_id = obj_id
        super().__init__(**kwargs)

    def refresh_metadata(self):
        """Refresh Metadata.

        Refreshes the property of metdata.

        Returns
            _metdata (dict): metadata from api

        """
        api_url = f"core/system/group/{self.obj_id}"
        resp_data = self.request_helper(api_url, method="get").json()
        self._metadata = resp_data['RequestedObject']
        return self._metadata

    def add_member(self, user_obj: UserClass):
        """Add member to group.

        Pass a User Object that you would like to add to this group

        Args:
            user_obj (pyarcher.user.User): Archer User Object

        Returns
            resp (requests.models.Response)

        """
        members = [member.obj_id for member in self.members]
        members.append(user_obj.obj_id)
        resp = self.update_group(self.metadata['Name'], child_users=members)
        user_obj.refresh_groups()
        return resp

    def remove_member(self, user_obj: UserClass):
        """Remove member from group.

        Pass a User Object that you would like to remove from this group

        Args:
            user_obj (pyarcher.user.User): Archer User Object

        Returns
            resp (requests.models.Response)

        """
        members = [
            member.obj_id
            for member in self.members
            if member.obj_id == user_obj.obj_id
        ]
        resp = self.update_group(self.metadata['Name'], child_users=members)
        user_obj.refresh_groups()
        return resp

    def add_parent_group(self, group_obj: GroupClass):
        """Add a parent group.

        Pass a Group Object that you would like this group to be a child of

        Args:
            group_obj (pyarcher.group.Group): Archer Group Object

        Returns
            resp (requests.models.Response)

        """
        parent_groups = [
            parent_group.obj_id
            for parent_group in self.parent_groups
        ]
        parent_groups.append(group_obj.obj_id)
        resp = self.update_group(
            self.metadata['Name'], parent_groups=parent_groups
        )
        group_obj.membership_setter()
        self.membership_setter()
        return resp

    def remove_parent_group(self, group_obj: GroupClass):
        """Remove a parent group.

        Pass a Group Object that you would like this group to be removed as a
        child

        Args:
            group_obj (pyarcher.group.Group): Archer Group Object

        Returns
            resp (requests.models.Response)

        """
        parent_groups = [
            parent_group.obj_id
            for parent_group in self.parent_groups
            if parent_group.obj_id == group_obj.obj_id
        ]
        resp = self.update_group(
            self.metadata['Name'], parent_groups=parent_groups
        )
        group_obj.membership_setter()
        self.membership_setter()
        return resp

    def add_child_group(self, group_obj: GroupClass):
        """Add child group.

        Pass a Group Object that you would like this group to be a parent of

        Args:
            group_obj (pyarcher.group.Group): Archer Group Object

        Returns
            resp (requests.models.Response)

        """
        resp =  self.archer.modify_child_group(
            self.obj_id, group_obj.obj_id, is_add=True
        )
        group_obj.membership_setter()
        return resp

    def remove_child_group(self, group_obj: GroupClass):
        """Remove child group.

        Pass a Group Object that you would like this group to remove being a
        parent of

        Args:
            group_obj (pyarcher.group.Group): Archer Group Object

        Returns
            resp (requests.models.Response)

        """
        resp =  self.archer.modify_child_group(
            self.obj_id, group_obj.obj_id, is_add=False
        )
        group_obj.membership_setter()
        return resp

    def add_role(self, role_id):
        """Add role to this group."""
        # TODO: Pass role obj
        return self.archer.modify_group_role(
            self.obj_id, role_id, is_add=True
        )

    def remove_role(self, role_id):
        """Remove role from this group."""
        # TODO: Pass role obj
        return self.archer.modify_group_role(
            self.obj_id, role_id, is_add=False
        )

    def delete(self):
        """Delete this group."""
        return self.archer.delete_group(self.obj_id)

    def update_group(
        self,
        name: str = None,
        parent_groups: list = None,
        child_groups: list = None,
        child_users: list = None
    ):
        """Update Group.

        Update this groups child groups, members, name, description, or parent
        groups.
        WARNING: This will not update other objects that are affected by this.

        Kwargs:
            See pyarcher.archer.update_group

        Returns:
            resp (requests.models.Response):

        """
        # TODO: convert to object and update all objects
        name = name or self.metadata['Name']

        def try_list_comp(objs):
            try:
                value = [obj.obj_id for obj in objs]
            except TypeError:
                value = None
            return value

        parent_groups = try_list_comp(parent_groups)
        child_groups = try_list_comp(child_groups)
        child_users = try_list_comp(child_users)

        resp = self.archer.update_group(
            self.obj_id,
            name,
            parent_groups=parent_groups,
            child_groups=child_groups,
            child_users=child_users
        )
        self.membership_setter()
        return resp

    def membership_setter(self):
        """Membership setter.

        This updates the parent_groups and members property. Archer does not
        have an individual api for this.

        """
        group_data = self.archer.group_membership_setter(self.obj_id)
        self.parent_groups = group_data['parent_groups']
        self.members = group_data['members']

    def child_setter(self):
        """Child property setter."""
        hierachy_data = self.archer.get_group_hierarchy()
        self.child_groups = hierachy_data.get(self.obj_id, [])
        return self.child_groups

    def get_all_members(self):
        _ids = set()
        users = []
        for child_group in self.child_groups:
            for member in child_group['group'].members:
                _ids.add(member.obj_id)
        for _id in _ids:
            users.append(
                self.archer.get_user(_id)
            )
        self.all_members = users

    @property
    def members(self):
        """Members property."""
        if not self._members:
            self.membership_setter()
        return self._members

    @members.setter
    def members(self, data):
        """Members property setter."""
        self._members = data
        return self._members

    @property
    def all_members(self):
        """All members including nest property."""
        if not self._all_members:
            self.get_all_members()
        return self._all_members

    @all_members.setter
    def all_members(self, data):
        self._all_members = data
        return self._members

    @property
    def archer(self):
        """Archer property."""
        archer = self.resource("archer")
        return archer

    @property
    def parent_groups(self):
        """Parent Groups property."""
        if not self._parent_groups:
            self.membership_setter()
        return self._parent_groups

    @parent_groups.setter
    def parent_groups(self, data):
        """Parent Groups property setter."""
        self._parent_groups = data

    @property
    def child_groups(self):
        """Child Groups property."""
        if not self._child_groups:
            return self.child_setter()
        return self._child_groups

    @child_groups.setter
    def child_groups(self, data):
        """Child Groups property setter."""
        self._child_groups = data