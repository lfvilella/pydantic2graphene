import pydantic
import graphene
import pydantic2graphene


class Human(pydantic.BaseModel):
    name: str


class HumanConverter(pydantic2graphene.ConverterToGrapheneBase):
    class Config:
        model = Human


class TestConverterToGrapheneBase:
    def test_returns_object_type_schema(self, normalize_sdl):
        value = HumanConverter.as_class(graphene.ObjectType)
        expected_value = """
            type HumanGql {
                name: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_when_graphene_type_is_not_set_use_object_type_as_default(
        self, normalize_sdl,
    ):
        value = HumanConverter.as_class()
        expected_value = """
            type HumanGql {
                name: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)
