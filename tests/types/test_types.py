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
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(list))

    def test_tuple_field(self, normalize_sdl):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(tuple))

    def test_dict_field(self, normalize_sdl):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(dict))

    def test_set_field(self, normalize_sdl):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(set))

    def test_frozenset_field(self, normalize_sdl):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(frozenset))

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
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(
                to_pydantic_class(datetime.timedelta)
            )

    def test_any_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(typing.Any))

    def test_type_var_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(
                to_pydantic_class(typing.TypeVar("custom_types"))
            )

    def test_optional_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(typing.Optional[int])
        )
        expected_value = """
            type FakeGql {
                field: Int
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_typing_list_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(typing.List[str])
        )
        expected_value = """
            type FakeGql {
                field: [String!]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_typing_tuple_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(typing.Tuple[str])
        )
        expected_value = """
            type FakeGql {
                field: [String!]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_typing_dict_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(
                to_pydantic_class(typing.Dict[str, str])
            )

    def test_typing_set_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(typing.Set[str])
        )
        expected_value = """
            type FakeGql {
                field: [String!]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_typing_frozenset_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(typing.FrozenSet[str])
        )
        expected_value = """
            type FakeGql {
                field: [String!]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_typing_sequence_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(typing.Sequence[str])
        )
        expected_value = """
            type FakeGql {
                field: [String!]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_typing_iterable_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(typing.Iterable[str])
        )
        expected_value = """
            type FakeGql {
                field: [String!]!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_typing_type_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(to_pydantic_class(typing.Type[str]))

    def test_typing_callable_field(self):
        with pytest.raises(pydantic2graphene.FieldNotSupported):
            pydantic2graphene.to_graphene(
                to_pydantic_class(typing.Callable[[int], str])
            )

    def test_typing_pattern_field(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(
            to_pydantic_class(typing.Pattern)
        )
        expected_value = """
            type FakeGql {
                field: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)
