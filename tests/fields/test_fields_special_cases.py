import datetime
import unittest.mock
import typing

import pytest
import pydantic
import pydantic2graphene


def to_pydantic_class(field_type):
    class Fake(pydantic.BaseModel):
        field: field_type

    return Fake


class TestDatetimeNotImplemented:
    def test_datetime_date_field_old_version(self, module_wrapper):
        import graphene.types.datetime

        fake_module = module_wrapper(graphene.types.datetime, exclude=["Date"])
        with unittest.mock.patch("graphene.types.datetime", fake_module):
            # graphene.types.datetime.Date is not present in the module
            with pytest.raises(pydantic2graphene.FieldNotSupported):
                pydantic2graphene.fields._TYPE_MAPPING = None
                pydantic2graphene.to_graphene(to_pydantic_class(datetime.date))

    def test_datetime_time_field(self, module_wrapper):
        import graphene.types.datetime

        fake_module = module_wrapper(graphene.types.datetime, exclude=["Time"])
        with unittest.mock.patch("graphene.types.datetime", fake_module):
            # graphene.types.datetime.Time is not present in the module
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


class TestPydanticIterableShapeNotAvailable:
    def test_do_not_raise_attribute_error(self, module_wrapper):
        import pydantic.fields
        import pydantic2graphene.fields

        fake_module = module_wrapper(
            pydantic.fields, exclude=["SHAPE_ITERABLE"]
        )
        with unittest.mock.patch("pydantic.fields", fake_module):
            pydantic2graphene.fields._LIST_SHAPES = None
            pydantic2graphene.fields.is_list_shape(None)

        assert (
            fake_module.wrapper_local_state.exceptions_counter[
                "SHAPE_ITERABLE"
            ]
            == 1
        )


@unittest.mock.patch("pydantic2graphene.converter.dataclasses", None)
class TestDataclassesNotAvailablePy36:
    def test_list_field_works(self, normalize_sdl):
        class Fake(pydantic.BaseModel):
            field: typing.List[str] = []

        value = pydantic2graphene.to_graphene(Fake)
        expected_value = """
            type FakeGql {
                field: [String]
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)
