# -*- coding: utf-8 -*-
"""Main module."""
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from pyarcher.group import Group
    from pyarcher.user import User
    from pyarcher.application import Application

GroupClass = TypeVar("GroupClass", bound="Group")
UserClass = TypeVar("UserClass", bound="User")
