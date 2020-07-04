import pytest
import pydantic
import graphene
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
