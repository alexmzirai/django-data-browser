# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_query_html context"] = {
    "config": {
        "adminUrl": "/admin/data_browser/view/add/",
        "allModelFields": {
            "auth.Group": {
                "fields": {
                    "admin": {"concrete": False, "model": None, "type": "html"},
                    "id": {"concrete": True, "model": "number", "type": "number"},
                    "name": {"concrete": True, "model": "string", "type": "string"},
                },
                "sortedFields": ["id", "admin", "name"],
            },
            "auth.User": {
                "fields": {
                    "admin": {"concrete": False, "model": None, "type": "html"},
                    "date_joined": {"concrete": True, "model": "time", "type": "time"},
                    "email": {"concrete": True, "model": "string", "type": "string"},
                    "first_name": {
                        "concrete": True,
                        "model": "string",
                        "type": "string",
                    },
                    "id": {"concrete": True, "model": "number", "type": "number"},
                    "is_active": {
                        "concrete": True,
                        "model": "boolean",
                        "type": "boolean",
                    },
                    "is_staff": {
                        "concrete": True,
                        "model": "boolean",
                        "type": "boolean",
                    },
                    "is_superuser": {
                        "concrete": True,
                        "model": "boolean",
                        "type": "boolean",
                    },
                    "last_login": {"concrete": True, "model": "time", "type": "time"},
                    "last_name": {
                        "concrete": True,
                        "model": "string",
                        "type": "string",
                    },
                    "password": {"concrete": True, "model": "string", "type": "string"},
                    "username": {"concrete": True, "model": "string", "type": "string"},
                },
                "sortedFields": [
                    "id",
                    "admin",
                    "date_joined",
                    "email",
                    "first_name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "last_login",
                    "last_name",
                    "password",
                    "username",
                ],
            },
            "boolean": {
                "fields": {
                    "average": {"concrete": False, "model": None, "type": "number"},
                    "sum": {"concrete": False, "model": None, "type": "number"},
                },
                "sortedFields": ["average", "sum"],
            },
            "data_browser.View": {
                "fields": {
                    "admin": {"concrete": False, "model": None, "type": "html"},
                    "created_time": {"concrete": True, "model": "time", "type": "time"},
                    "description": {
                        "concrete": True,
                        "model": "string",
                        "type": "string",
                    },
                    "fields": {"concrete": True, "model": "string", "type": "string"},
                    "google_sheets_formula": {
                        "concrete": False,
                        "model": None,
                        "type": "string",
                    },
                    "id": {"concrete": True, "model": "string", "type": "string"},
                    "model_name": {
                        "concrete": True,
                        "model": "string",
                        "type": "string",
                    },
                    "name": {"concrete": True, "model": "string", "type": "string"},
                    "open_view": {"concrete": False, "model": None, "type": "string"},
                    "owner": {"concrete": False, "model": "auth.User", "type": None},
                    "public": {"concrete": True, "model": "boolean", "type": "boolean"},
                    "public_link": {"concrete": False, "model": None, "type": "string"},
                    "query": {"concrete": True, "model": "string", "type": "string"},
                },
                "sortedFields": [
                    "id",
                    "admin",
                    "created_time",
                    "description",
                    "fields",
                    "google_sheets_formula",
                    "model_name",
                    "name",
                    "open_view",
                    "owner",
                    "public",
                    "public_link",
                    "query",
                ],
            },
            "html": {"fields": {}, "sortedFields": []},
            "number": {
                "fields": {
                    "average": {"concrete": False, "model": None, "type": "number"},
                    "count": {"concrete": False, "model": None, "type": "number"},
                    "max": {"concrete": False, "model": None, "type": "number"},
                    "min": {"concrete": False, "model": None, "type": "number"},
                    "std_dev": {"concrete": False, "model": None, "type": "number"},
                    "sum": {"concrete": False, "model": None, "type": "number"},
                    "variance": {"concrete": False, "model": None, "type": "number"},
                },
                "sortedFields": [
                    "average",
                    "count",
                    "max",
                    "min",
                    "std_dev",
                    "sum",
                    "variance",
                ],
            },
            "string": {
                "fields": {
                    "count": {"concrete": False, "model": None, "type": "number"}
                },
                "sortedFields": ["count"],
            },
            "tests.Address": {
                "fields": {
                    "admin": {"concrete": False, "model": None, "type": "html"},
                    "city": {"concrete": True, "model": "string", "type": "string"},
                    "id": {"concrete": True, "model": "number", "type": "number"},
                },
                "sortedFields": ["id", "admin", "city"],
            },
            "tests.InAdmin": {
                "fields": {
                    "admin": {"concrete": False, "model": None, "type": "html"},
                    "id": {"concrete": True, "model": "number", "type": "number"},
                    "name": {"concrete": True, "model": "string", "type": "string"},
                },
                "sortedFields": ["id", "admin", "name"],
            },
            "tests.InlineAdmin": {
                "fields": {
                    "id": {"concrete": True, "model": "number", "type": "number"},
                    "in_admin": {
                        "concrete": False,
                        "model": "tests.InAdmin",
                        "type": None,
                    },
                    "name": {"concrete": True, "model": "string", "type": "string"},
                },
                "sortedFields": ["id", "in_admin", "name"],
            },
            "tests.Normal": {
                "fields": {
                    "admin": {"concrete": False, "model": None, "type": "html"},
                    "id": {"concrete": True, "model": "number", "type": "number"},
                    "in_admin": {
                        "concrete": False,
                        "model": "tests.InAdmin",
                        "type": None,
                    },
                    "inline_admin": {
                        "concrete": False,
                        "model": "tests.InlineAdmin",
                        "type": None,
                    },
                    "name": {"concrete": True, "model": "string", "type": "string"},
                },
                "sortedFields": ["id", "admin", "in_admin", "inline_admin", "name"],
            },
            "tests.Producer": {
                "fields": {
                    "address": {
                        "concrete": False,
                        "model": "tests.Address",
                        "type": None,
                    },
                    "admin": {"concrete": False, "model": None, "type": "html"},
                    "id": {"concrete": True, "model": "number", "type": "number"},
                    "name": {"concrete": True, "model": "string", "type": "string"},
                },
                "sortedFields": ["id", "admin", "address", "name"],
            },
            "tests.Product": {
                "fields": {
                    "admin": {"concrete": False, "model": None, "type": "html"},
                    "default_sku": {
                        "concrete": False,
                        "model": "tests.SKU",
                        "type": None,
                    },
                    "id": {"concrete": True, "model": "number", "type": "number"},
                    "is_onsale": {"concrete": False, "model": None, "type": "string"},
                    "name": {"concrete": True, "model": "string", "type": "string"},
                    "onsale": {"concrete": True, "model": "boolean", "type": "boolean"},
                    "producer": {
                        "concrete": False,
                        "model": "tests.Producer",
                        "type": None,
                    },
                    "size": {"concrete": True, "model": "number", "type": "number"},
                    "size_unit": {
                        "concrete": True,
                        "model": "string",
                        "type": "string",
                    },
                },
                "sortedFields": [
                    "id",
                    "admin",
                    "default_sku",
                    "is_onsale",
                    "name",
                    "onsale",
                    "producer",
                    "size",
                    "size_unit",
                ],
            },
            "tests.SKU": {
                "fields": {
                    "admin": {"concrete": False, "model": None, "type": "html"},
                    "id": {"concrete": True, "model": "number", "type": "number"},
                    "name": {"concrete": True, "model": "string", "type": "string"},
                    "product": {
                        "concrete": False,
                        "model": "tests.Product",
                        "type": None,
                    },
                },
                "sortedFields": ["id", "admin", "name", "product"],
            },
            "tests.Tag": {
                "fields": {
                    "admin": {"concrete": False, "model": None, "type": "html"},
                    "id": {"concrete": True, "model": "number", "type": "number"},
                    "name": {"concrete": True, "model": "string", "type": "string"},
                },
                "sortedFields": ["id", "admin", "name"],
            },
            "time": {
                "fields": {
                    "count": {"concrete": False, "model": None, "type": "number"}
                },
                "sortedFields": ["count"],
            },
        },
        "baseUrl": "/data_browser/",
        "savedViews": [],
        "sortedModels": [
            "auth.Group",
            "auth.User",
            "data_browser.View",
            "tests.Address",
            "tests.InAdmin",
            "tests.InlineAdmin",
            "tests.Normal",
            "tests.Producer",
            "tests.Product",
            "tests.SKU",
            "tests.Tag",
        ],
        "types": {
            "boolean": {
                "defaultLookup": "equals",
                "defaultValue": True,
                "lookups": {
                    "equals": {"type": "boolean"},
                    "is_null": {"type": "boolean"},
                    "not_equals": {"type": "boolean"},
                },
                "sortedLookups": ["equals", "not_equals", "is_null"],
            },
            "html": {
                "defaultLookup": None,
                "defaultValue": None,
                "lookups": {},
                "sortedLookups": [],
            },
            "number": {
                "defaultLookup": "equals",
                "defaultValue": 0,
                "lookups": {
                    "equals": {"type": "number"},
                    "gt": {"type": "number"},
                    "gte": {"type": "number"},
                    "is_null": {"type": "boolean"},
                    "lt": {"type": "number"},
                    "lte": {"type": "number"},
                    "not_equals": {"type": "number"},
                },
                "sortedLookups": [
                    "equals",
                    "not_equals",
                    "gt",
                    "gte",
                    "lt",
                    "lte",
                    "is_null",
                ],
            },
            "string": {
                "defaultLookup": "equals",
                "defaultValue": "",
                "lookups": {
                    "contains": {"type": "string"},
                    "ends_with": {"type": "string"},
                    "equals": {"type": "string"},
                    "is_null": {"type": "boolean"},
                    "not_contains": {"type": "string"},
                    "not_ends_with": {"type": "string"},
                    "not_equals": {"type": "string"},
                    "not_regex": {"type": "string"},
                    "not_starts_with": {"type": "string"},
                    "regex": {"type": "string"},
                    "starts_with": {"type": "string"},
                },
                "sortedLookups": [
                    "equals",
                    "contains",
                    "starts_with",
                    "ends_with",
                    "regex",
                    "not_equals",
                    "not_contains",
                    "not_starts_with",
                    "not_ends_with",
                    "not_regex",
                    "is_null",
                ],
            },
            "time": {
                "defaultLookup": "equals",
                "defaultValue": "redacted",
                "lookups": {
                    "equals": {"type": "time"},
                    "gt": {"type": "time"},
                    "gte": {"type": "time"},
                    "is_null": {"type": "boolean"},
                    "lt": {"type": "time"},
                    "lte": {"type": "time"},
                    "not_equals": {"type": "time"},
                },
                "sortedLookups": [
                    "equals",
                    "not_equals",
                    "gt",
                    "gte",
                    "lt",
                    "lte",
                    "is_null",
                ],
            },
        },
        "version": "redacted",
    },
    "initialState": {
        "fields": [
            {"path": "size", "priority": 0, "sort": "dsc"},
            {"path": "name", "priority": 1, "sort": "asc"},
            {"path": "size_unit", "priority": None, "sort": None},
        ],
        "filters": [
            {"errorMessage": None, "lookup": "lt", "path": "size", "value": "2"},
            {"errorMessage": None, "lookup": "gt", "path": "id", "value": "0"},
        ],
        "model": "tests.Product",
        "results": [],
    },
    "sentryDsn": None,
}
