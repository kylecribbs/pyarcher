# -*- coding: utf-8 -*-

"""Main module."""
import logging

import requests

from pyarcher.user import User
from pyarcher.group import Group
from pyarcher.application import Application
from pyarcher.base import ArcherBase

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class Archer(ArcherBase):
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

    def refresh_metadata(self):
        """Refresh Metadata."""
        pass

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

    def user(self, user_id):
        to_pass = self._pass_archer_base()
        to_pass['user_id'] = user_id
        user = User(**to_pass)
        return user

    def query_users(self, params: dict, raw=False):
        """Query for Users

        Args:
            params (dict): Send a dictionary of ODATA Params without the "$".
                Example: params['filter'] = "AccountStatus eq '1'"

        Returns:
            requests.models.Response: The response of the http call from
                requests.
        """
        if "Id" not in params.get(
            "select",
            "Id,DisplayName,FirstName,LastName"
        ):
            params['select'] = f"Id,{params['select']}"

        params = {f"${key}": value for key, value in params.items()}
        resp = self.request_helper(
            "core/system/user/",
            method="get",
            params=params
        )
        resp_data = resp.json()
        if raw:
            return resp
        return [self.user(user['RequestedObject']['Id']) for user in resp_data]

    def create_user(
        self,
        username: str,
        first_name: str,
        last_name: str,
        password: str,
        account_status: int = 1
    ):
        data = {
            "User": {
                "FirstName": first_name,
                "LastName": last_name,
                "Username": username,
            },
            "Password": password
        }

        resp = self.request_helper(
            "core/system/user",
            method="post",
            data=data
        )

        return resp

    def group(self, obj_id):
        return self.factory(obj_id, Group)

    def all_groups(self) -> dict:
        resp = self.request_helper("core/system/group/", method="get")
        resp_data = resp.json()
        groups = []
        for group in resp_data:
            new_group = self.group(group["RequestedObject"]["Id"])
            new_group.metadata(group["RequestedObject"])
            groups.append(new_group)
        return groups


    def get_active_users_with_no_login(self):
        params = {
            "select": "Id,UserName,DisplayName",
            "filter": "AccountStatus eq '1'and LastLoginDate eq null",
            "orderby": "LastName"
        }
        return self.query_users(params)

    def application(self, obj_id):
        return self.factory(obj_id, Application)

    def all_application(self):
        resp = self.request_helper("core/system/application/", method="get")
        resp_data = resp.json()
        return [
            self.application(app['RequestedObject']['Id']) for app in resp_data
        ]

    def create_content_record(self, fields_json, record_id=None):
        """
        :param fields_json: {field name how you see it in the app: value content
                                        (for text it text, for others it's internal unique ids)}
        :param record_id:
        :returns int - record_id
        """
        api_url = f"{self.api_url_base}core/content/"
        post_header = dict(self.header)

        transformed_json = {}
        for key in fields_json.keys():
            current_key_id = self.get_field_id_by_name(key)
            transformed_json[current_key_id] = self.add_value_to_field(current_key_id, fields_json[key])

        if record_id:
            post_header["X-Http-Method-Override"] = "PUT"
            body = json.dumps({"Content": {"Id": record_id, "LevelId": self.application_level_id,
                                           "FieldContents": transformed_json}})
        else:
            post_header["X-Http-Method-Override"] = "POST"
            body = json.dumps({"Content": {"LevelId": self.application_level_id, "FieldContents": transformed_json}})

        try:
            if record_id:
                response = requests.put(api_url, headers=post_header, data=body, verify=False)
                data = json.loads(response.content.decode("utf-8"))
                log.info("Record updated, %s", data["RequestedObject"]["Id"])
            else:
                response = requests.post(api_url, headers=post_header, data=body, verify=False)
                data = json.loads(response.content.decode("utf-8"))
                log.info("Function create_content_record created record, %s", data["RequestedObject"]["Id"])

            return data["RequestedObject"]["Id"]

        except Exception as e:
            log.info("Function create_content_record didn't work, %s", e)

    def create_sub_record(self, fields_json, subform_name):
        """LevelID is an application
                :param fields_json: {field name how you see it in the app: value content
                                        (for text it text, for others it's internal unique ids)}
                :param subform_name: how you see it in the app
                :returns sub_record_id
        """
        api_url = f"{self.api_url_base}core/content/"
        post_header = dict(self.header)
        post_header["X-Http-Method-Override"] = "POST"

        subform_field_id = self.get_field_id_by_name(subform_name)

        transformed_json = {}
        for key in fields_json.keys():
            current_id = self.subforms_json_by_sf_name[subform_name][key]
            current_json = dict(self.subforms_json_by_sf_name[subform_name][current_id])
            current_json["Value"] = fields_json[key]
            subform_level_id = self.subforms_json_by_sf_name[subform_name]["LevelId"]
            transformed_json.update({current_id: current_json})

        body = json.dumps({"Content": {"LevelId": subform_level_id, "FieldContents": transformed_json},
                           "SubformFieldId": subform_field_id})

        try:
            response = requests.post(api_url, headers=post_header, data=body, verify=False)
            data = json.loads(response.content.decode("utf-8"))

            log.info("Function create_sub_record created record, %s", data["RequestedObject"]["Id"])

            return data["RequestedObject"]["Id"]

        except Exception as e:
            log.error("Function create_sub_record didn't work, %s", e)

    def post_attachment(self, name, base64_string):
        """
        :param name: Name of the attachment
        :param base64_string: File in base64_string
        :return:
        """
        api_url = f"{self.api_url_base}core/content/attachment"
        post_header = dict(self.header)
        post_header["X-Http-Method-Override"] = "POST"
        body = json.dumps({"AttachmentName": name, "AttachmentBytes": base64_string})

        try:
            response = requests.post(api_url, headers=post_header, data=body, verify=False)
            data = response.json()

            log.info("Attachment %s posted to Archer", data["RequestedObject"]["Id"])
            return data["RequestedObject"]["Id"]

        except Exception as e:
            log.error("Function post_attachment didn't work, %s; Response content: %s", e, response.content)

    def update_content_record(self, updated_json, record_id):
        """LevelID is an application
        :param updated_json: see function create_content_record()
        :param record_id: internal archer ID
        :returns record_id
        """
        return self.create_content_record(updated_json, record_id)

    def get_record(self, record_id):
        """
        :param record_id: internal archer record id
        :return: record object
        """
        api_url = f"{self.api_url_base}core/content/fieldcontent/"
        cont_id = [str(record_id)]
        body = json.dumps({"FieldIds": self.all_application_fields_array, "ContentIds": cont_id})

        post_header = dict(self.header)
        post_header["X-Http-Method-Override"] = "POST"

        try:
            response = requests.post(api_url, headers=post_header, data=body, verify=False)
            data = json.loads(response.content.decode("utf-8"))

            return Record(self, data[0]["RequestedObject"])

        except Exception as e:
            log.error("Function get_record() didn't work, %s", e)

    def get_sub_record(self, sub_record_id, sub_record_name):
        """
        :param sub_record_id:
        :param sub_record_name:
        :return: record object
        """
        api_url = f"{self.api_url_base}core/content/fieldcontent/"
        cont_id = [str(sub_record_id)]
        all_fields_arr = self.subforms_json_by_sf_name[sub_record_name]["AllFields"]
        body = json.dumps({"FieldIds": all_fields_arr, "ContentIds": cont_id})

        post_header = dict(self.header)
        post_header["X-Http-Method-Override"] = "POST"

        try:
            response = requests.post(api_url, headers=post_header, data=body, verify=False)
            data = json.loads(response.content.decode("utf-8"))

            return Record(self, data[0]["RequestedObject"])

        except Exception as e:
            log.error("Function get_sub_record() didn't work, %s", e)


    def all_endpoints(self):
        """
        :param app_name: Try a name you see in the app
        :return: You will get printout of all similar grc_api endpoints urls that
                 might be slightly different from the app name, don't ask me why.
                 For all grc_api calls use the name you get.
        """

        resp = self.request_helper("", content_api=True, method="get")
        return resp.json()['value']

    def records(self):
        pass

    def get_grc_endpoint_records(self, endpoint_url, skip=None):
        """
        By default gets 1000 records from the endpoint.
        :param endpoint_url: get from find_grc_endpoint_url()
        :param skip: number of records to skip in thousands (1,2,3)
        :return: array of record jsons
        """
        if skip:
            api_url = self.content_api_url_base + endpoint_url + "?$skip=" + str(skip)

        else:
            api_url = self.content_api_url_base + endpoint_url

        response = requests.get(api_url, headers=self.header, verify=False)
        data = json.loads(response.content.decode("utf-8"))
        array_jsons = []

        for record in data["value"]:
            array_jsons.append(record)

        return array_jsons

    def build_unique_value_to_id_mapping(self, endpoint_url, key_value_field=None, prefix=None):
        """
        :param endpoint_url: get from find_grc_endpoint_url()
        :param key_value_field: name of the field with unique value that you
                        identified in your application(e.g. "Incident #")
        :param prefix: adding prefix in front of key_value_field, sometimes in Archer
                         tranp_key fields are shown like INC-xxx, but in app they only have xxx,
                         so to solve that add prefix here, in our case it's INC-
        :return: Populate Archer_Instance object with self.key_field_value_to_system_id with {field_value:content_record_id}
        """

        i = 0
        for_equal_numbers = 0  # breaks out of the loop if the number of records are equal to 1000
        all_records = []

        while True:
            current_records = self.get_grc_endpoint_records(endpoint_url, i)
            all_records += current_records
            if len(current_records) != 1000 or for_equal_numbers > 21: # Attention, if records are more than 21000 increase the value
                break

            i += 1000
            for_equal_numbers += 1

        for record in all_records:
            if key_value_field:
                if prefix:
                    field_value = prefix + str(record[key_value_field])
                else:
                    field_value = str(record[key_value_field])

                system_id = record[endpoint_url + "_Id"]
                self.key_field_value_to_system_id.update({field_value: system_id})

            else:
                print(record)
                print('Please choose your key_field above: {"KEY_FIELD": "unique value"}')
                break

        log.info("Updated the mapping between record id and KEY_FIELD")

    def get_record_id_by_unique_value(self, key_value_field):
        """
        :param key_value_field: field you used in build_unique_value_to_id_mapping()
        :return: record id or False
        """
        try:
            return self.key_field_value_to_system_id[key_value_field]
        except:
            return False

    def add_record_id_to_mapping(self, key_value_field, system_id, prefix=None):
        """
        :param key_value_field: field you used in build_unique_value_to_id_mapping()
        :param system_id: redord id
        :param prefix:
        :return: populate self.key_field_value_to_system_id
        """
        if prefix:
            field_value = prefix + str(key_value_field)
        else:
            field_value = str(key_value_field)

        self.key_field_value_to_system_id.update({field_value: system_id})
