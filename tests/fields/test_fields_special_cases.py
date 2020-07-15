import collections
import datetime
import unittest.mock

import pytest
import pydantic
import pydantic2graphene


def to_pydantic_class(field_type):
    class Fake(pydantic.BaseModel):
        field: field_type

    return Fake


@unittest.mock.patch(
    "graphene.types.datetime",
    collections.namedtuple("fake_module", "DateTime")(None),
)
class TestDatetimeNotImplemented:
    def test_datetime_date_field_old_version(self):
        # graphene.types.datetime.Date is not present in the module
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.fields._TYPE_MAPPING = None
            pydantic2graphene.to_graphene(to_pydantic_class(datetime.date))

    def test_datetime_time_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.fields._TYPE_MAPPING = None
            pydantic2graphene.to_graphene(to_pydantic_class(datetime.time))


class FakeEmailStr(str):
    pass


@unittest.mock.patch("pydantic.EmailStr", FakeEmailStr)
@unittest.mock.patch("pydantic.NameEmail", FakeEmailStr)
class TestPydanticEmailFieldNotAvailable:
    def test_pydantic_email_str_field(self, normalize_sdl):
        pydantic2graphene.fields._TYPE_MAPPING = None
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.EmailStr)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_pydantic_name_email_field(self, normalize_sdl):
        pydantic2graphene.fields._TYPE_MAPPING = None
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(pydantic.NameEmail)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)


class FakeConList(str):
    pass


@unittest.mock.patch("pydantic.conlist", FakeConList)
class TestPydanticConListFieldNotAvailable:
    def test_pydantic_conlist_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(pydantic.conlist))
