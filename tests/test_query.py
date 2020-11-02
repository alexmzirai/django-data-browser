from datetime import date, datetime, timedelta

import pytest
from django.http import QueryDict
from django.utils import timezone

from data_browser import orm_fields
from data_browser.orm_admin import OrmModel, get_fields_for_type
from data_browser.query import BoundQuery, Query, QueryField, QueryFilter
from data_browser.types import (
    ASC,
    DSC,
    BooleanType,
    DateTimeType,
    DateType,
    DurationType,
    HTMLType,
    IsNullType,
    MonthType,
    NumberChoiceType,
    NumberType,
    StringChoiceType,
    StringType,
    UnknownType,
    WeekDayType,
    YearType,
)

from .util import ANY


@pytest.fixture
def query():
    return Query(
        "app.model",
        [
            QueryField("fa", False, ASC, 1),
            QueryField("fd", False, DSC, 0),
            QueryField("fn"),
        ],
        [QueryFilter("bob", "equals", "fred")],
    )


@pytest.fixture
def orm_models():
    return {
        "string": OrmModel(get_fields_for_type(StringType)),
        "number": OrmModel(get_fields_for_type(NumberType)),
        "app.model": orm_fields.OrmModel(
            fields={
                "fa": orm_fields.OrmConcreteField(
                    model_name="app.model",
                    name="fa",
                    pretty_name="fa",
                    type_=StringType,
                    rel_name=StringType.name,
                ),
                "fd": orm_fields.OrmConcreteField(
                    model_name="app.model",
                    name="fd",
                    pretty_name="fd",
                    type_=StringType,
                    rel_name=StringType.name,
                ),
                "fn": orm_fields.OrmCalculatedField(
                    model_name="app.model", name="fn", pretty_name="fn", func=None
                ),
                "bob": orm_fields.OrmConcreteField(
                    model_name="app.model",
                    name="bob",
                    pretty_name="bob",
                    type_=StringType,
                    rel_name=StringType.name,
                ),
                "num": orm_fields.OrmConcreteField(
                    model_name="app.model",
                    name="num",
                    pretty_name="num",
                    type_=NumberType,
                    rel_name=NumberType.name,
                ),
                "tom": orm_fields.OrmFkField(
                    model_name="app.model",
                    name="tom",
                    pretty_name="tom",
                    rel_name="app.Tom",
                ),
            },
            admin=True,
        ),
        "app.Tom": orm_fields.OrmModel(
            fields={
                "jones": orm_fields.OrmConcreteField(
                    model_name="app.Tom",
                    name="jones",
                    pretty_name="jones",
                    type_=StringType,
                    rel_name=StringType.name,
                ),
                "michael": orm_fields.OrmFkField(
                    model_name="app.Tom",
                    name="michael",
                    pretty_name="michael",
                    rel_name="app.Michael",
                ),
            },
            admin=True,
        ),
        "app.Michael": orm_fields.OrmModel(
            fields={
                "bolton": orm_fields.OrmConcreteField(
                    model_name="app.Michael",
                    name="bolton",
                    pretty_name="bolton",
                    type_=StringType,
                    rel_name=StringType.name,
                )
            },
            admin=True,
        ),
    }


@pytest.fixture
def bound_query(query, orm_models):
    return BoundQuery.bind(query, orm_models)


class TestQuery:
    def test_from_request(self, query):
        q = Query.from_request(
            "app.model", "fa+1,fd-0,fn", QueryDict("bob__equals=fred")
        )
        assert q == query

    def test_from_request_duplicate_field(self, query):
        q = Query.from_request(
            "app.model", "fa+1,fd-0,fn,&fa-2", QueryDict("bob__equals=fred")
        )
        assert q == query

    def test_from_request_with_limit(self, query):
        q = Query.from_request(
            "app.model", "fa+1,fd-0,fn", QueryDict("limit=123&bob__equals=fred")
        )
        query.limit = 123
        assert q == query

    def test_from_request_with_bad_limit(self, query):
        q = Query.from_request(
            "app.model", "fa+1,fd-0,fn", QueryDict("limit=bob&bob__equals=fred")
        )
        query.limit = 1000
        assert q == query

    def test_from_request_with_low_limit(self, query):
        q = Query.from_request(
            "app.model", "fa+1,fd-0,fn", QueryDict("limit=0&bob__equals=fred")
        )
        query.limit = 1
        assert q == query

    def test_from_request_with_related_filter(self):
        q = Query.from_request("app.model", "", QueryDict("bob__jones__equals=fred"))
        assert q == Query(
            "app.model", [], [QueryFilter("bob__jones", "equals", "fred")]
        )

    def test_from_request_with_missing(self):
        q = Query.from_request("app.model", ",,", QueryDict(""))
        assert q == Query("app.model", [], [])

    def test_from_request_filter_no_value(self):
        q = Query.from_request("app.model", "", QueryDict("joe__equals="))
        assert q == Query("app.model", [], [QueryFilter("joe", "equals", "")])

    def test_from_request_filter_no_lookup(self):
        q = Query.from_request("app.model", "", QueryDict("joe=tom"))
        assert q == Query("app.model", [], [])

    def test_from_request_filter_bad_lookup(self):
        q = Query.from_request("app.model", "", QueryDict("joe__blah=123"))
        assert q == Query("app.model", [], [QueryFilter("joe", "blah", "123")])

    def test_from_request_filter_no_name(self):
        q = Query.from_request("app.model", "", QueryDict("=123"))
        assert q == Query("app.model", [], [])

    def test_from_request_field_no_name(self):
        q = Query.from_request("app.model", "+2", QueryDict(""))
        assert q == Query("app.model", [QueryField("", False, ASC, 2)], [])

    def test_from_request_field_no_priority(self):
        q = Query.from_request("app.model", "fn+", QueryDict(""))
        assert q == Query("app.model", [QueryField("fn")], [])

    def test_from_request_field_bad_priority(self):
        q = Query.from_request("app.model", "fn+x", QueryDict(""))
        assert q == Query("app.model", [QueryField("fn")], [])

    def test_from_request_field_pivoted(self):
        q = Query.from_request("app.model", "&fn", QueryDict(""))
        assert q == Query("app.model", [QueryField("fn", True)], [])

    def test_url(self, query):
        query.limit = 123
        assert (
            query.get_url("html")
            == "/data_browser/query/app.model/fa+1,fd-0,fn.html?bob__equals=fred&limit=123"
        )

    def test_url_no_filters(self, query):
        query.filters = []
        assert (
            query.get_url("html")
            == "/data_browser/query/app.model/fa+1,fd-0,fn.html?limit=1000"
        )


class TestBoundQuery:
    def test_fields(self, bound_query):
        assert [f.path for f in bound_query.fields] == [["fa"], ["fd"], ["fn"]]

    def test_sort_fields(self, bound_query):
        assert [(f.path, f.direction, f.priority) for f in bound_query.sort_fields] == [
            (["fd"], DSC, 0),
            (["fa"], ASC, 1),
        ]

    def test_bad_field(self, orm_models):
        query = Query("app.model", [QueryField("yata")], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_bad_field_lookup(self, orm_models):
        query = Query("app.model", [QueryField("fa__count__bob")], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_bad_fk(self, orm_models):
        query = Query("app.model", [QueryField("yata__yata")], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_bad_fk_field(self, orm_models):
        query = Query("app.model", [QueryField("tom__yata")], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_bad_fk_field_aggregate(self, orm_models):
        query = Query("app.model", [QueryField("tom__jones__yata")], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_bad_long_fk(self, orm_models):
        query = Query("app.model", [QueryField("yata__yata__yata")], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_aggregate(self, orm_models):
        query = Query("app.model", [QueryField("tom__jones__count")], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.fields] == [["tom", "jones", "count"]]

    def test_piovt_aggregate(self, orm_models):
        query = Query("app.model", [QueryField("tom__jones__count", pivoted=True)], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.pivoted for f in bound_query.fields] == [False]

    def test_piovt(self, orm_models):
        query = Query("app.model", [QueryField("tom__jones", pivoted=True)], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.pivoted for f in bound_query.fields] == [True]

    def test_bad_filter(self, orm_models):
        query = Query("app.model", [], [QueryFilter("yata", "equals", "fred")])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.filters] == []

    def test_bad_filter_value(self, orm_models):
        query = Query(
            "app.model",
            [],
            [QueryFilter("num", "equals", "fred"), QueryFilter("num", "equals", 1)],
        )
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.value for f in bound_query.filters] == ["fred", 1]
        assert [f.value for f in bound_query.valid_filters] == [1]

    def test_fk(self, orm_models):
        query = Query("app.model", [QueryField("tom")], [])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.fields] == []

    def test_filter_calculated_field(self, orm_models):
        query = Query("app.model", [], [QueryFilter("fn", "equals", "fred")])
        bound_query = BoundQuery.bind(query, orm_models)
        assert [f.path for f in bound_query.filters] == []


class TestType:
    def test_repr(self):
        assert repr(StringType) == f"StringType"


class TestStringType:
    @pytest.mark.django_db
    def test_validate(self):
        assert StringType.parse("contains", "hello") == ("hello", None)
        assert StringType.parse("pontains", "hello") == (None, ANY(str))
        assert StringType.parse("regex", ".*") == (".*", None)
        assert StringType.parse("regex", "\\") == (None, ANY(str))

    def test_default_lookup(self):
        assert StringType.default_lookup == "equals"

    def test_format(self):
        assert StringType.get_formatter(None)("bob") == "bob"
        assert StringType.get_formatter(None)(None) is None


class TestNumberType:
    def test_validate(self):
        assert NumberType.parse("gt", "6.1") == (6.1, None)
        assert NumberType.parse("pontains", "6.1") == (None, ANY(str))
        assert NumberType.parse("gt", "hello") == (None, ANY(str))
        assert NumberType.parse("is_null", "True") == (True, None)
        assert NumberType.parse("is_null", "hello") == (None, ANY(str))

    def test_default_lookup(self):
        assert NumberType.default_lookup == "equals"

    def test_format(self):
        assert NumberType.get_formatter(None)(6) == 6
        assert NumberType.get_formatter(None)(None) is None


class TestYearType:
    def test_validate(self):
        assert YearType.parse("gt", "6") == (6, None)
        assert YearType.parse("pontains", "6.1") == (None, ANY(str))
        assert YearType.parse("gt", "hello") == (None, ANY(str))
        assert YearType.parse("is_null", "True") == (True, None)
        assert YearType.parse("is_null", "hello") == (None, ANY(str))
        assert YearType.parse("equals", "0") == (None, ANY(str))

    def test_default_lookup(self):
        assert YearType.default_lookup == "equals"

    def test_format(self):
        assert YearType.get_formatter(None)(6) == 6
        assert YearType.get_formatter(None)(None) is None


class TestDateTimeType:
    def test_validate(self):
        assert DateTimeType.parse("gt", "2018-03-20T22:31:23") == (ANY(datetime), None)
        assert DateTimeType.parse("gt", "hello") == (None, ANY(str))
        assert DateTimeType.parse("pontains", "2018-03-20T22:31:23") == (None, ANY(str))
        assert DateTimeType.parse("is_null", "True") == (True, None)
        assert DateTimeType.parse("is_null", "hello") == (None, ANY(str))
        assert DateTimeType.parse("gt", "now") == (ANY(datetime), None)
        assert DateTimeType.parse("gt", "11-22-2018") == (ANY(datetime), None)
        assert DateTimeType.parse("gt", "21-12-2018") == (ANY(datetime), None)
        assert DateTimeType.parse("gt", "11-12-2018") == (None, ANY(str))
        assert DateTimeType.parse("gt", "21-22-2018") == (None, ANY(str))

    def test_default_lookup(self):
        assert DateTimeType.default_lookup == "equals"

    @pytest.mark.django_db
    def test_aware_format(self, settings):
        settings.USE_TZ = True
        assert (
            DateTimeType.get_formatter(None)(
                datetime(2020, 5, 19, 8, 42, 16, tzinfo=timezone.utc)
            )
            == "2020-05-19 08:42:16"
        )
        assert DateTimeType.get_formatter(None)(None) is None

    @pytest.mark.django_db
    def test_naive_format(self, settings):
        settings.USE_TZ = False
        assert (
            DateTimeType.get_formatter(None)(datetime(2020, 5, 19, 8, 42, 16))
            == "2020-05-19 08:42:16"
        )
        assert DateTimeType.get_formatter(None)(None) is None


class TestDurationType:
    def test_validate(self):
        assert DurationType.parse("gt", "5 days") == (timedelta(days=5), None)
        assert DurationType.parse("gt", "5 5:5") == (
            timedelta(days=5, hours=5, minutes=5),
            None,
        )
        assert DurationType.parse("gt", "5 dayss") == (None, ANY(str))
        assert DurationType.parse("pontains", "5 days") == (None, ANY(str))
        assert DurationType.parse("is_null", "True") == (True, None)
        assert DurationType.parse("is_null", "hello") == (None, ANY(str))

    def test_default_lookup(self):
        assert DurationType.default_lookup == "equals"

    def test_format(self):
        assert (
            DurationType.get_formatter(None)(timedelta(days=5, minutes=6))
            == "5 days, 0:06:00"
        )
        assert DurationType.get_formatter(None)(timedelta(minutes=6)) == "0:06:00"
        assert DurationType.get_formatter(None)(None) is None


class TestDateType:
    def test_validate(self):
        assert DateType.parse("gt", "2018-03-20T22:31:23") == (ANY(date), None)
        assert DateType.parse("gt", "hello") == (None, ANY(str))
        assert DateType.parse("pontains", "2018-03-20T22:31:23") == (None, ANY(str))
        assert DateType.parse("is_null", "True") == (True, None)
        assert DateType.parse("is_null", "hello") == (None, ANY(str))
        assert DateType.parse("gt", "today") == (ANY(date), None)
        assert DateType.parse("gt", "11-22-2018") == (ANY(date), None)
        assert DateType.parse("gt", "21-12-2018") == (ANY(date), None)
        assert DateType.parse("gt", "11-12-2018") == (None, ANY(str))
        assert DateType.parse("gt", "21-22-2018") == (None, ANY(str))

    def test_default_lookup(self):
        assert DateType.default_lookup == "equals"

    def test_format(self):
        assert DateType.get_formatter(None)(date(2020, 5, 19)) == "2020-05-19"
        assert DateType.get_formatter(None)(None) is None


class TestWeekDayType:
    def test_validate(self):
        assert WeekDayType.parse("equals", "Sunday") == (1, None)
        assert WeekDayType.parse("equals", "Saturday") == (7, None)
        assert WeekDayType.parse("equals", "Bob") == (None, ANY(str))
        assert WeekDayType.parse("gt", "Monday") == (None, ANY(str))

    def test_format(self):
        assert WeekDayType.get_formatter(None)(1) == "Sunday"
        assert WeekDayType.get_formatter(None)(7) == "Saturday"
        assert WeekDayType.get_formatter(None)(None) is None

    def test_default_lookup(self):
        assert WeekDayType.default_lookup == "equals"


class TestMonthType:
    def test_validate(self):
        assert MonthType.parse("equals", "January") == (1, None)
        assert MonthType.parse("equals", "December") == (12, None)
        assert MonthType.parse("equals", "Bob") == (None, ANY(str))
        assert MonthType.parse("gt", "January") == (None, ANY(str))

    def test_format(self):
        assert MonthType.get_formatter(None)(1) == "January"
        assert MonthType.get_formatter(None)(12) == "December"
        assert MonthType.get_formatter(None)(None) is None

    def test_default_lookup(self):
        assert MonthType.default_lookup == "equals"


class TestBooleanType:
    def test_validate(self):
        assert BooleanType.parse("equals", "True") == (True, None)
        assert BooleanType.parse("equals", "False") == (False, None)
        assert BooleanType.parse("equals", "hello") == (None, ANY(str))
        assert BooleanType.parse("pontains", "True") == (None, ANY(str))

    def test_format(self):
        assert BooleanType.get_formatter(None)(None) is None

    def test_default_lookup(self):
        assert BooleanType.default_lookup == "equals"


class TestStringChoiceType:
    def test_format(self):
        assert (
            StringChoiceType.get_formatter([("a", "A"), ("b", "B"), ("c", "C")])("b")
            == "B"
        )
        assert (
            StringChoiceType.get_formatter([("a", "A"), ("b", "B"), ("c", "C")])(None)
            is None
        )

    def test_bad_value(self):
        assert (
            StringChoiceType.get_formatter([("a", "A"), ("b", "B"), ("c", "C")])("x")
            == "x"
        )


class TestNumberChoiceType:
    def test_format(self):
        assert NumberChoiceType.get_formatter([(1, "A"), (2, "B"), (3, "C")])(2) == "B"
        assert (
            NumberChoiceType.get_formatter([(1, "A"), (2, "B"), (3, "C")])(None) is None
        )

    def test_bad_value(self):
        assert NumberChoiceType.get_formatter([(1, "A"), (2, "B"), (3, "C")])(6) == 6


class TestHTMLType:
    def test_format(self):
        assert HTMLType.get_formatter(None)(None) is None


class TestIsNullType:
    def test_format(self):
        assert IsNullType.get_formatter(None)(True) == "IsNull"
        assert IsNullType.get_formatter(None)(False) == "NotNull"
        assert IsNullType.get_formatter(None)(None) is None


class TestUnknownType:
    def test_format(self):
        assert UnknownType.get_formatter(None)(None) is None
