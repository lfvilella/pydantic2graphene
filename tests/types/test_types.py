import pytest
import typing
import datetime
import pydantic
import pydantic2graphene


def to_pydantic_class(field_type):
    class Fake(pydantic.BaseModel):
        field: field_type

    return Fake


class TestTypeMappingPydantic2Graphene:
    def test_string_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(to_pydantic_class(str))
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_int_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(to_pydantic_class(int))
        expected_value = """
            type FakeGql {
                field: Int!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_float_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(to_pydantic_class(float))
        expected_value = """
            type FakeGql {
                field: Float!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_boolean_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(to_pydantic_class(bool))
        expected_value = """
            type FakeGql {
                field: Boolean!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_bytes_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(to_pydantic_class(bytes))
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_list_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(to_pydantic_class(list))
        expected_value = """
            type FakeGql {
                field: [String]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_tuple_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(to_pydantic_class(tuple))
        expected_value = """
            type FakeGql {
                field: [String]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_dict_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(to_pydantic_class(dict))
        expected_value = """
            type FakeGql {
                field: [String]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_set_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(to_pydantic_class(set))
        expected_value = """
            type FakeGql {
                field: [String]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_frozenset_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(to_pydantic_class(frozenset))
        expected_value = """
            type FakeGql {
                field: [String]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_datetime_date_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(to_pydantic_class(datetime.date))
        expected_value = """
            scalarDatetypeFakeGql {
                field: Date!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_datetime_datetime_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(datetime.datetime)
        )
        expected_value = """
            scalarDateTimetypeFakeGql {
                field: DateTime!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_datetime_time_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(to_pydantic_class(datetime.time))
        expected_value = """
            type FakeGql {
                field: Time!
            }scalarTime
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_datetime_timedelta_field(self):
        with pytest.raises(pydantic2graphene.errors.FieldNotSupported):
            pydantic2graphene.to_graphene(
                to_pydantic_class(datetime.timedelta)
            )

    def test_any_field(self):
        with pytest.raises(pydantic2graphene.errors.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(typing.Any))

    def test_type_var_field(self):
        with pytest.raises(pydantic2graphene.errors.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(typing.TypeVar('custom_types')))

    def test_optional_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(to_pydantic_class(typing.Optional[int]))
        expected_value = """
            type FakeGql {
                field: Int
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)
