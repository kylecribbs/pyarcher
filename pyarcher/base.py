# -*- coding: utf-8 -*-

"""Main module."""
import logging
from abc import ABCMeta, abstractmethod
from typing import Dict

import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class ArcherBase(metaclass=ABCMeta):
    """Creates archer instance object using following arguments

    A username and password or a cert and key must be passed to initiate an
    archer instance.

    Args:
        url (str): Full path url to archer instance.
            example: https://archer.com/rsarcher
        instance_name (str): Archer instance name.
        user_domain (optional, str)
        username (optional, str): Username to login with.
        password (optional, str): Password to login with.
        client_cert (optional, tuple(str, str)): Tuple of cert and key file
            path.

    Attributes:

    """

    _metdata: dict = None

    def __init__(
        self,
        url: str,
        instance_name: str,
        user_domain: str = None,
        username: str = None,
        password: str = None,
        client_cert: tuple = None,
        session_token: str = None,
    ):
        """Init."""
        self.logger = logging.getLogger(__name__)

        self.url = url
        self.instance_name = instance_name
        self.user_domain = user_domain
        self.username = username
        self.password = password
        self.session_token = session_token

        self.api_url_base = f"{self.url}/api/"
        self.content_api_url_base = f"{self.url}/contentapi/"
        self.platform_api_url_base = f"{self.url}/platformapi/"

        self.session = requests.Session()
        self.session.cert = client_cert

    def request_helper(
        self,
        path: str,
        method: str = "post",
        method_override: str = None,
        accept: str = "application/json,text/html,application/xhtml+xml,application/xml;q =0.9,*/*;q=0.8",
        content_type: str = "application/json",
        content_api: bool = False,
        platform_api: bool = False,
        data: dict = None,
        params: dict = None,
        verify: bool = False
    ):
        """An RSA Archer request helper.

        Args:
            path (str): API route
            method (str, optional): Requests method function.
                Defaults to "post".
            method_override (str, optional): Archer best practice is to use
                method override by doing a POST and overriding with a GET.
                Defaults to None.
            accept (str, optional): Accept header.
                Defaults to "application/json,text/html,application/xhtml+xml,application/xml;q =0.9,*/*;q=0.8".
            content_type (str, optional): Content-Type header.
                Defaults to "application/json".
            content_api (bool, optional): Flag for specifying if contentapi
                should be used instead of api.
                Defaults to False.
            data (dict, optional): Body of the http call.
                Defaults to None.
            params (dict, optional): Params are passed to request to be
                urlencoded.
                Defaults to None.
            verify (bool): Verify path to CA's.
                Defaults to False.

        Returns:
            requests.models.Response: The response of the http call from
                requests.
        """
        headers = dict()
        headers["Accept"] = accept
        headers["Content-Type"] = content_type
        if self.session_token:
            headers["Authorization"] = "Archer session-id={}".format(
                self.session_token
            )
        if method_override:
            headers['X-Http-Method-Override'] = method_override

        self.session.headers = headers

        base_url = self.api_url_base
        if content_api:
            base_url = self.content_api_url_base
        elif platform_api:
            base_url = self.platform_api_url_base

        url = f"{base_url}{path}"
        call = getattr(self.session, method)
        resp = call(url, json=data, params=params)
        # resp_data = resp.json()
        # if isinstance(resp_data, list):
        #     for data in resp_data:
        #         self.check_error(data)
        # else:
        #     self.check_error(resp_data)

        return resp

    def check_error(self, data: Dict):
        """Check Error from response data."""
        if not data['IsSuccessful']:
            for error in data['ValidationMessages']:
                self.logger.error(error['Description'])
                print("error")
                return True
        return False

    def login(self, sso: bool = False):
        """Login for RSA Archer.

        Args:
            sso (bool): Use single sign on or not. Default False.

        Returns:
            requests.models.Response: The response of the http call from
                requests.
        """
        if sso:
            base_url = self.api_url_base
            self.api_url_base = f"{self.url}/Default.aspx"

            response = self.request_helper("", method="get")

            self.api_url_base = base_url
            return response

        data = {
            "InstanceName": self.instance_name,
            "Username": self.username,
            "Password": self.password
        }
        data["UserDomain"] = ""
        if self.user_domain:
            data["UserDomain"] = self.user_domain

        resp = self.request_helper("core/security/login", data=data)

        resp_data = resp.json()
        self.session_token = resp_data["RequestedObject"]["SessionToken"]
        return resp

    def logout(self):
        """Archer Logout."""
        # TODO: Create logout
        pass

    def factory(self, obj_id, obj):
        to_pass = self._pass_archer_base()
        to_pass['obj_id'] = obj_id
        pass_obj = obj(**to_pass)
        return pass_obj

    def _pass_archer_base(self):
        to_pass = [
            "url", "instance_name", "user_domain", "username", "password",
            "client_cert", "session_token"
        ]
        to_pass_dict = {
            key: value
            for key, value in self.__dict__.items()
            if key in to_pass and value
        }
        return to_pass_dict

    @abstractmethod
    def refresh_metadata(self):
        """Refresh Metadata Abstract Method."""

    @property
    def metadata(self):
        """Property method for metadata."""
        if not self._metadata:
            self._metadata = self.refresh_metadata()
        return self._metadata

    @metadata.setter
    def metadata(self, data: dict) -> dict:
        self._metadata = data
        return self._metadata


    @property
    def exists(self):
        exist = False
        if self.metadata:
            exist = True
        return exist
