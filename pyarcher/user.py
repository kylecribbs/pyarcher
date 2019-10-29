# -*- coding: utf-8 -*-

"""User module."""
from dataclasses import dataclass

from pyarcher.archer import Archer


@dataclass
class User(Archer):
    """[summary].

    Args:
        Archer ([type]): [description]

    Returns:
        [type]: [description]

    """

    user_id: int
    _email: list = None
    _display_name: str = None
    _username: str = None
    _last_login_date: str = None

    def __post_init__(self, *args, **kwargs):
        """Post Init"""
        super().__init__(*args, **kwargs)


    def get_user_details(self):
        """
        :param user_id: internal Archer user id
        :return: User object
        """
        api_url = f"core/system/user/{self.user_id}"
        resp_data = self.request_helper(api_url, method="get").json()
        # TODO: set self attributes from resp

    def capture_user_email(self):
        api_url = f"{self.archer_instance.api_url_base}core/system/usercontact/{self.user_id}"
        try:
            response = requests.get(api_url, headers=self.archer_instance.header, verify=False)
            if response.status_code != 200:
                self.email = ""
                log.debug("Cannot load email for user ID %s", self.user_id)
            else:
                data = json.loads(response.content.decode("utf-8"))
                self.email = data[0]["RequestedObject"]["Value"]

        except Exception as e:
            self.email =""
            log.error("Exception %s. Guess there is no email for user %s", e, self.json["DisplayName"])

    @property
    def email(self):
        """Property method for Email"""
        if not self._email:
            self.get_user_details()
        return self._email

    @property
    def display_name(self):
        """Property method for Display Name"""
        if not self._display_name:
            self.get_user_details()
        return self._display_name

    @property
    def username(self):
        """Property method for Username"""
        if not self._username:
            self.get_user_details()
        return self._username

    @property
    def last_login_date(self):
        """Property method for Last Login Date"""
        if not self._last_login_date:
            self.get_user_details()
        return self._last_login_date

    def assign_role(self, role_id):
        """
        :param role_id: internal system id
        :return: log message of success oe failure
        """
        api_url = f"{self.archer_instance.api_url_base}core/system/userrole"
        request_body = {"UserId": f"{self.user_id}", "RoleId": f"{role_id}", "IsAdd": "true"}

        try:
            response = requests.put(api_url, headers=self.archer_instance.header, json=request_body, verify=False)
            if response.status_code != 200:
                log.error("User with ID %s can not be added a role %s", self.user_id, role_id)
            else:
                log.info("User %s assigned a role_id %s", self.get_user_email(), role_id)
        except Exception as e:
            log.error("Exception %s", e)

    def assign_group(self, group):
        """
        :param group: Name of the group how you see it in Archer
        :return: log message of success oe failure
        """
        group_id = self.archer_instance.get_group_id(group) #just in case

        api_url = f"{self.archer_instance.api_url_base}core/system/usergroup"
        request_body = {"UserId": f"{self.user_id}", "GroupId": f"{group_id}", "IsAdd": "true"}

        try:
            response = requests.put(api_url, headers=self.archer_instance.header, json=request_body, verify=False)
            if response.status_code != 200:
                print(response)
                log.error("User %s can not be added to a group %s", self.get_user_email(), group)
            else:
                log.info("User %s assigned to a group %s", self.get_user_email(), group)
        except Exception as e:
            log.error("Exception %s", e)

    def activate_user(self):
        """
        :return: log message of success or failure
        """
        post_header = dict(self.archer_instance.header)
        del post_header["X-Http-Method-Override"]

        api_url = f"{self.archer_instance.api_url_base}core/system/user/status/active/{self.user_id}"

        try:
            response = requests.post(api_url, headers=post_header, verify=False)
            if response.status_code != 200:
                print(response)
                log.error("User %s can not be activated", self.user_id)
            else:
                log.info("User %s is activated", self.get_gisplay_name())
        except Exception as e:
            log.error("Exception in activate_user() %s", e)

    def deactivate_user(self):
        """
        :return: log message of success or failure
        """
        post_header = dict(self.archer_instance.header)
        del post_header["X-Http-Method-Override"]

        api_url = f"{self.archer_instance.api_url_base}core/system/user/status/inactive/{self.user_id}"

        try:
            response = requests.post(api_url, headers=post_header, verify=False)
            if response.status_code != 200:
                print(response)
                log.error("User %s can not be deactivated", self.user_id)
            else:
                log.info("User %s is deactivated", self.get_gisplay_name())
        except Exception as e:
            log.error("Exception in deactivate_user() %s", e)