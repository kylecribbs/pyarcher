"""Stubber for stubber.json."""
import json

import requests


def stubber(request):
    """Generate Stubber."""
    try:
        with open(f"stubber.json", "rb") as file:
            data = json.loads(file.read())
    except FileNotFoundError:
        data = JSON

    routes = ["api", "contentapi", "platformapi"]

    resp = requests.Response()
    path_url = request.path_url.rstrip("/")
    exact_route = data.get(path_url, dict())
    exact_method = None
    if not exact_route:
        for route in routes:
            split_path_url = path_url.split("/")
            if route == split_path_url[1]:
                continue
            split_path_url[1] = route
            path_url = "/".join(split_path_url)
            exact_route = data.get(path_url, dict())
            if exact_route:
                break

    exact_method = exact_route.get(request.method, dict())
    exact_status_code = exact_method.get("status_code", dict())

    if exact_method:
        resp._content = bytes(
            json.dumps(exact_method.get("response")),
            "utf-8"
        )
        resp.status_code = exact_status_code if exact_status_code else 200
        return resp

    return None


JSON = {
    "/api/core/security/login": {
        "POST": {
            "response": {
                "Links": [],
                "RequestedObject": {
                    "SessionToken": "C204E18D0ED58E288533F39C455A36E8"
                },
                "IsSuccessful": True,
                "ValidationMessages": []
            },
            "status_code": 200
        }
    },
    "/api/core/security/logout": {
        "POST": {
            "response": {
                "Links": [],
                "RequestedObject": {

                },
                "IsSuccessful": True,
                "ValidationMessages": []
            },
            "status_code": 200
        }
    },
    "/platformapi/core/system/group/1": {
        "GET": {
            "response": {
                "Links": [],
                "RequestedObject": {
                    "Id": 1,
                    "Name": "NewGroupName",
                    "DisplayName": "NewGroupName",
                    "Description": "<html><head></head><pstyle=\"margin:0px\">NewGroup Description</p></html>",
                    "EveryoneFlag": False,
                    "Guid": "6dc2e265-2796-4e3c-ab8e-549ba03422d8",
                    "SystemFlag": False,
                    "LdapFlag": False,
                    "DomainId": None,
                    "DistinguishedName": None,
                    "DefaultHomeDashboardId":-1,
                    "DefaultHomeWorkspaceId":-1,
                    "UpdateInformation": {
                        "CreateDate": "2016-09-21T18:04:02.643",
                        "UpdateDate": "2016-09-21T18:06:51.027",
                        "CreateLogin": 1470,
                        "UpdateLogin": 1470
                    }
                },
                "IsSuccessful": True,
                "ValidationMessages": []
            },
            "status_code": 200
        },
        "DELETE": {
            "response": {
                "Links": [],
                "RequestedObject": {
                    "Id": 1
                },
                "IsSuccessful": True,
                "ValidationMessages": []
            },
            "status_code": 200
        }
    },
    "/platformapi/core/system/groupmember": {
        "GET": {
            "response": {
                "Links": [],
                "RequestedObject": {
                    "Id": 1
                },
                "IsSuccessful": True,
                "ValidationMessages": []
            },
            "status_code": 200
        },
        "PUT": {
            "response": {
                "Links": [],
                "RequestedObject": {
                    "Id": 1
                },
                "IsSuccessful": True,
                "ValidationMessages": []
            },
            "status_code": 200
        }
    },
    "/platformapi/core/system/rolegroup": {
        "PUT": {
            "response": {
                "Links": [],
                "RequestedObject": {
                    "Id": 1
                },
                "IsSuccessful": True,
                "ValidationMessages": []
            },
            "status_code": 200
        }
    },
    "/platformapi/core/system/group": {
        "GET": {
            "response": [
                {
                    "Links": [],
                    "RequestedObject": {
                        "Id": 1,
                        "Name": "NewGroupName",
                        "DisplayName": "NewGroupName",
                        "Description": "<html><head></head><pstyle=\"margin:0px\">NewGroup Description</p></html>",
                        "EveryoneFlag": False,
                        "Guid": "6dc2e265-2796-4e3c-ab8e-549ba03422d8",
                        "SystemFlag": False,
                        "LdapFlag": False,
                        "DomainId": None,
                        "DistinguishedName": None,
                        "DefaultHomeDashboardId":-1,
                        "DefaultHomeWorkspaceId":-1,
                        "UpdateInformation": {
                            "CreateDate": "2016-09-21T18:04:02.643",
                            "UpdateDate": "2016-09-21T18:06:51.027",
                            "CreateLogin": 1470,
                            "UpdateLogin": 1470
                        }
                    },
                    "IsSuccessful": True,
                    "ValidationMessages": []
                },
                {
                    "Links": [],
                    "RequestedObject": {
                        "Id": 1,
                        "Name": "UpdatedGroupName",
                        "DisplayName": "UpdatedGroupName",
                        "Description": "<html><head></head><pstyle=\"margin:0px\">WAS:NewGroup Description</p></html>",
                        "EveryoneFlag": False,
                        "Guid": "4eec52f1-bc2f-4460-ac2b-e6e179b5744d",
                        "SystemFlag": False,
                        "LdapFlag": False,
                        "DomainId": None,
                        "DistinguishedName": None,
                        "DefaultHomeDashboardId": None,
                        "DefaultHomeWorkspaceId": None,
                        "UpdateInformation": {
                            "CreateDate": "2016-09-22T16:07:59.807",
                            "UpdateDate": "2016-09-22T16:09:01.083",
                            "CreateLogin": 1470,
                            "UpdateLogin": 1230
                        }
                    },
                    "IsSuccessful": True,
                    "ValidationMessages": []
                }
            ],
            "status_code": 200
        },
        "PUT": {
            "response": {
                "Links": [],
                "RequestedObject": {
                    "Id": 1
                },
                "IsSuccessful": True,
                "ValidationMessages": []
            },
            "status_code": 200
        },
        "POST": {
            "response": {
                "Links": [],
                "RequestedObject": {
                    "Id": 1
                },
                "IsSuccessful": True,
                "ValidationMessages": []
            },
            "status_code": 200
        }
    },
    "/platformapi/core/system/grouphierarchy": {
        "GET": {
            "response": [
                {
                    "Links": [],
                    "RequestedObject": {
                        "Id": 1,
                        "RelatedId": 1,
                        "Generation":0
                    },
                    "IsSuccessful": True,
                    "ValidationMessages": []
                }
            ],
            "status_code": 200
        }
    },
    "/platformapi/core/system/groupmembership": {
        "GET": {
            "response": [
                {
                    "Links": [],
                    "RequestedObject": {
                        "GroupId": 1,
                        "UserIds": [1],
                        "ParentGroupIds": None
                    },
                    "IsSuccessful": True,
                    "ValidationMessages": []
                }
            ],
            "status_code": 200
        }
    },
    "/platformapi/core/system/group/user/1": {
        "GET": {
            "response": [
                {
                    "Links": [],
                    "RequestedObject": {
                        "Id": 1,
                        "Name": "AssetCatalogAdministator",
                        "DisplayName": "AssetCatalogAdministator",
                        "Description": "<html><head></head><pstyle=\"margin:0px\">TheAssetCatalog Administratorgroupisforuserswhohavefulladministrativeaccesstothefollowingcore applications:Applications,Devices,StorageDevices,Technologies,Business Processes,CorporateObjectives,ProductsandServices,InformationAssets,Facilities, andContacts.</p></html>",
                        "EveryoneFlag": False,
                        "Guid": "44690160-29e2-4b31-8c98-68cb5f0d014a",
                        "SystemFlag": False,
                        "LdapFlag": False,
                        "DomainId": None,
                        "DistinguishedName": None,
                        "DefaultHomeDashboardId": None,
                        "DefaultHomeWorkspaceId": None,
                        "UpdateInformation": {
                            "CreateDate": "2016-05-26T13:41:11.677",
                            "UpdateDate": "2016-05-26T13:41:11.677",
                            "CreateLogin": 2,
                            "UpdateLogin": 2
                        }
                    },
                    "IsSuccessful": True,
                    "ValidationMessages": []
                }
            ],
            "status_code": 200
        }
    },
    "/platformapi/core/system/group/user/0": {
        "GET": {
            "response": [
                {
                    "Links": [],
                    "RequestedObject": {},
                    "IsSuccessful": False,
                    "ValidationMessages": [
                        {
                            "Reason": "WebApi:WebApiResourceNotFoundQueryReason",
                            "Severity":3,
                            "MessageKey": "WebApi:WebApiResourceNotFoundQuery",
                            "Description": "Theresourcecannotbefound.",
                            "Location":-1,
                            "ErroredValue": None,
                            "Validator": "ArcherApi.Controllers.System.UserGroupController,ArcherApi, Version=6.2.100.1061,Culture=neutral,PublicKeyToken=None",
                            "XmlData": None,
                            "ResourcedMessage": "Noresourcefound."
                        }
                    ]
                }
            ],
            "status_code": 200
        }
    },
    "/platformapi/core/system/level": {
        "GET": {
            "response": {},
            "status_code": 200
        }
    },
    "/platformapi/core/system/level/1": {
        "GET": {
            "response": {},
            "status_code": 200
        }
    },
    "/platformapi/core/system/level/module/1": {
        "GET": {
            "response": {},
            "status_code": 200
        }
    },
    "/platformapi/core/system/level/referencefield/1": {
        "GET": {
            "response": {},
            "status_code": 200
        }
    },
    "/platformapi/core/system/levellayout/level/1": {
        "GET": {
            "response": {},
            "status_code": 200
        }
    },
    "/platformapi/core/system/questionnaire": {
        "GET": {
            "response": {},
            "status_code": 200
        }
    },
    "/platformapi/core/system/questionnaire/1": {
        "GET": {
            "response": {},
            "status_code": 200
        }
    },
    "/platformapi/core/system/questionnairerule/level/1": {
        "GET": {
            "response": {},
            "status_code": 200
        }
    },
    "/platformapi/core/system/role": {
        "GET": {
            "response": {},
            "status_code": 200
        },
        "PUT": {
            "response": {},
            "status_code": 200
        }
    },
    "/platformapi/core/system/role/1": {
        "GET": {
            "response": {},
            "status_code": 200
        },
        "DELETE": {
            "response": {},
            "status_code": 200
        }
    },
    "/platformapi/core/system/rolemembership": {
        "GET": {
            "response": {},
            "status_code": 200
        }
    },
    "/platformapi/core/system/role/user/1": {
        "GET": {
            "response": {},
            "status_code": 200
        }
    },
    "/platformapi/core/system/securityparameter": {
        "POST": {
            "response": {},
            "status_code": 200
        },
        "GET": {
            "response": {},
            "status_code": 200
        },
        "PUT": {
            "response": {},
            "status_code": 200
        }
    },
    "/platformapi/core/system/securityparameter/1": {
        "DELETE": {
            "response": {},
            "status_code": 200
        },
        "GET": {
            "response": {},
            "status_code": 200
        }
    },
    "/platformapi/core/system/usergroupselection/usergrouplist/1": {
        "GET": {
            "response": {},
            "status_code": 200
        }
    },
    "/platformapi/core/system/subform/1": {
        "GET": {
            "response": {},
            "status_code": 200
        }
    },
    "/platformapi/core/system/user/status/active/1": {
        "POST": {
            "response": {
                "Links": [],
                "RequestedObject": {
                    "Id": 1
                },
                "IsSuccessful": True,
                "ValidationMessages": []
            },
            "status_code": 200
        }
    },
    "/platformapi/core/system/user/status/inactive/1": {
        "POST": {
            "response": {
                "Links": [],
                "RequestedObject": {
                    "Id": 1
                },
                "IsSuccessful": True,
                "ValidationMessages": []
            },
            "status_code": 200
        }
    },
    "/platformapi/core/system/userrole": {
        "PUT": {
            "response": {
                "Links": [],
                "RequestedObject": {
                    "Id": 1
                },
                "IsSuccessful": True,
                "ValidationMessages": []
            },
            "status_code": 200
        }
    },
    "/platformapi/core/system/usergroup": {
        "PUT": {
            "response": {
                "Links": [],
                "RequestedObject": {
                    "Id": 1
                },
                "IsSuccessful": True,
                "ValidationMessages": []
            },
            "status_code": 200
        }
    },
    "/platformapi/core/system/userpassword": {
        "PUT": {
            "response": {
                "Links": [],
                "RequestedObject": {},
                "IsSuccessful": True,
                "ValidationMessages": []
            },
            "status_code": 200
        }
    },
    "/platformapi/core/system/user": {
        "POST": {
            "response": {
                "Links": [],
                "RequestedObject": {
                    "Id": 1
                },
                "IsSuccessful": True,
                "ValidationMessages": []
            },
            "status_code": 200
        },
        "GET": {
            "response": [
                {
                    "Links": [],
                    "RequestedObject": {
                        "Id": 1,
                        "DisplayName": "Archer,Eric",
                        "FirstName": "Eric",
                        "MiddleName": "",
                        "LastName": "Archer",
                        "LastLoginDate": "2016-07-28T17:19:01.137",
                        "UserName": "ericsc",
                        "AccountStatus": 1,
                        "DomainId": None,
                        "SecurityId":6,
                        "Locale": "en-US",
                        "TimeZoneId": "EasternStandardTime",
                        "Address": "",
                        "Company": "",
                        "Title": "",
                        "AdditionalNote": None,
                        "BusinessUnit": None,
                        "Department": None,
                        "ForcePasswordChange": False,
                        "DistinguishedName": None,
                        "Type": 1,
                        "LanguageId": None,
                        "DefaultHomeDashboardId":-1,
                        "DefaultHomeWorkspaceId":-1,
                        "UpdateInformation": {
                            "CreateDate": "2015-06-29T17:12:29.107",
                            "UpdateDate": "2016-07-18T20:01:12.333",
                            "CreateLogin": 2,
                            "UpdateLogin": 229
                        }
                    },
                    "IsSuccessful": True,
                    "ValidationMessages": []
                }
            ],
            "status_code": 200
        },
        "PUT": {
            "response": {
                "Links": [],
                "RequestedObject": {
                    "Id": 1
                },
                "IsSuccessful": True,
                "ValidationMessages": []
            },
            "status_code": 200
        }
    },
    "/platformapi/core/system/user/1": {
        "DELETE": {
            "response": {
                "Links": [],
                "RequestedObject": {
                    "Id": 1
                },
                "IsSuccessful": True,
                "ValidationMessages": []
            },
            "status_code": 200
        },
        "GET": {
            "response": {
                "Links": [],
                "RequestedObject": {
                    "Id": 1,
                    "DisplayName": "Archer,Eric",
                    "FirstName": "Eric",
                    "MiddleName": "",
                    "LastName": "Archer",
                    "LastLoginDate": "2016-07-28T17:19:01.137",
                    "UserName": "ericsc",
                    "AccountStatus": 1,
                    "DomainId": None,
                    "SecurityId":6,
                    "Locale": "en-US",
                    "TimeZoneId": "EasternStandardTime",
                    "Address": "",
                    "Company": "",
                    "Title": "",
                    "AdditionalNote": None,
                    "BusinessUnit": None,
                    "Department": None,
                    "ForcePasswordChange": False,
                    "DistinguishedName": None,
                    "Type": 1,
                    "LanguageId": None,
                    "DefaultHomeDashboardId":-1,
                    "DefaultHomeWorkspaceId":-1,
                    "UpdateInformation": {
                        "CreateDate": "2015-06-29T17:12:29.107",
                        "UpdateDate": "2016-07-18T20:01:12.333",
                        "CreateLogin": 2,
                        "UpdateLogin": 229
                    }
                },
                "IsSuccessful": True,
                "ValidationMessages": []
            },
            "status_code": 200
        }
    },
    "/platformapi/core/system/usercontact": {
        "GET": {
            "response": [
                {
                    "Links": [],
                    "RequestedObject": {
                        "UserId": 1,
                        "Contacts": [
                            {
                                "ContactType": 7,
                                "ContactSubType": 2,
                                "IsDefault": True,
                                "Value": "example@domain.com",
                                "Id": 1
                            }
                        ]
                    },
                    "IsSuccessful": True,
                    "ValidationMessages": []
                }
            ],
            "status_code": 200
        }
    },
    "/platformapi/core/system/usercontact/1": {
        "GET": {
            "response": [
                {
                    "Links": [],
                    "RequestedObject": {
                        "ContactType": 7,
                        "ContactSubType": 2,
                        "IsDefault": True,
                        "Value": "example@domain.com",
                        "Id": 1
                    },
                    "IsSuccessful": True,
                    "ValidationMessages": []
                }
            ],
            "status_code": 200
        }
    },
    "/platformapi/core/system/user/group/1": {
        "GET": {
            "response": [
                {
                    "Links": [],
                    "RequestedObject": {
                        "Id": 1,
                        "DisplayName": "Doe,John",
                        "FirstName": "John",
                        "MiddleName": None,
                        "LastName": "Doe",
                        "LastLoginDate": "2016-09-13T15:16:18.35",
                        "UserName": "doej",
                        "AccountStatus": 1,
                        "DomainId": None,
                        "SecurityId": 1,
                        "Locale": None,
                        "TimeZoneId": "EasternStandardTime",
                        "Address": None,
                        "Company": None,
                        "Title": None,
                        "AdditionalNote": None,
                        "BusinessUnit": None,
                        "Department": None,
                        "ForcePasswordChange": False,
                        "DistinguishedName": None,
                        "Type": 1,
                        "LanguageId": None,
                        "DefaultHomeDashboardId": -1,
                        "DefaultHomeWorkspaceId": -1,
                        "UpdateInformation": {
                            "CreateDate": "2016-09-12T19:30:49.043",
                            "UpdateDate": "2016-09-13T17:54:48.807",
                            "CreateLogin": 2,
                            "UpdateLogin": 2
                        }
                    },
                    "IsSuccessful": True,
                    "ValidationMessages": []
                }
            ],
            "status_code": 200
        }
    },
    "/platformapi/core/system/task": {
        "GET": {
            "response": [
                {
                    "Links": [],
                    "RequestedObject": {
                        "TaskId": 234137,
                        "Title": "ExceptionRequestSubmissionPendingFor2",
                        "Description": "Theexceptionrequest2requiresinputandsubmissiontothereviewer.",
                        "DueDate": "2018-05-31T00:00:00",
                        "IsComplete": False,
                        "TargetContentId": 234136
                    },
                    "IsSuccessful": True,
                    "ValidationMessages": []
                },
                {
                    "Links": [],
                    "RequestedObject": {
                        "TaskId": 235439,
                        "Title": "ExceptionRequestSubmissionPendingFor3",
                        "Description": "Theexceptionrequest3requiresinputandsubmissiontothereviewer.",
                        "DueDate": "2018-07-22T00:00:00",
                        "IsComplete": False,
                        "TargetContentId": 235438
                    },
                    "IsSuccessful": True,
                    "ValidationMessages": []
                }
            ],
            "status_code": 200
        }
    },
    "/platformapi/core/system/valueslist/1": {
        "GET": {
            "response": {},
            "status_code": 200
        }
    },
    "/platformapi/core/system/valueslistvalue/valueslist/1": {
        "GET": {
            "response": {},
            "status_code": 200
        }
    },
    "/contentapi/Applications": {
        "GET": {
            "response": {
                "@odata.context": "localhost/contentapi/$metadata/$metadata#Risk_ Register",
                "value": [
                    {
                        "Risk_Register_Id": 107826,
                        "Actual_Annualized_Loss_Amount": 0,
                        "Actual_Response_Date": None,
                        "Adjusted_Qual_Residual_Risk": [
                            "NotRated"
                        ],
                        "Adjusted_Qual_Risk_Impact": [
                            "NotRated"
                        ],
                        "Adjusted_Qual_Risk_Likelihood": [
                            "NotRated"
                        ],
                        "Adjusted_Quantitative_Residual_Risk": [
                            "NotRated"
                        ],
                        "Adjusted_Quantitative_Risk_Helper": 0,
                        "Annual_Inherent_Risk": 0,
                        "Annual_Loss_Expectancy": 0,
                        "Annual_Residual_Risk": 0,
                        "Applications_Risk_Register": [],
                        "Assessment_Approach": [],
                        "Average_Cost_of_Controls": 0,
                        "Average_Loss_Amount": 0,
                        "Business_Processes_Risk_Register": [],
                        "Business_Units": [],
                        "Company_Objectives": [],
                        "Content_Source": [
                            "RSA Archer"
                        ]
                    }
                ]
            },
            "status_code": 200
        }
    },
    "/contentapi/Incidents_Risks": {
        "GET": {
            "response": {
                "@odata.context": "localhost/contentapi/Incidents_ Risks/$metadata#Incidents_Risks",
                "value": [
                    {
                        "Incidents_Id": 224931,
                        "Risk_Register_Id": 224961
                    },
                    {
                        "Incidents_Id": 224931,
                        "Risk_Register_Id": 224962
                    }
                ]
            },
            "status_code": 200
        }
    },
    "/contentapi/Exception_Requests": {
        "POST": {
            "response": {},
            "status_code": 200
        }
    },
    "/api/core/system/WorkflowAction/1": {
        "POST": {
            "response": {
                "Links": [],
                "RequestedObject": {
                    "WorkflowNodeId": "18304:CUST",
                    "WorkflowNodeName": "ExceptionRequests:57",
                    "JobStatus": "Running",
                    "Actions": [
                        {
                            "WorkflowTransitionId": "2221:CUST",
                            "WorkflowTransitionName": "Deny",
                            "CompletionCode": 10
                        },
                        {
                            "WorkflowTransitionId": "2222:CUST",
                            "WorkflowTransitionName": "Reject",
                            "CompletionCode": 2
                        },
                        {
                            "WorkflowTransitionId": "2247:CUST",
                            "WorkflowTransitionName": "Approve",
                            "CompletionCode": 1
                        },
                        {
                            "WorkflowTransitionId": "2256:CUST",
                            "WorkflowTransitionName": "ReAssignStakeholders",
                            "CompletionCode": 3
                        }
                    ]
                },
                "IsSuccessful": True,
                "ValidationMessages": []
            },
            "status_code": 200
        }
    },
    "/api/core/system/WorkflowAction": {
        "POST": {
            "response": {},
            "status_code": 200
        }
    },
    "/api/core/system/application": {
        "GET": {
            "response": {},
            "status_code": 200
        }
    }
}
