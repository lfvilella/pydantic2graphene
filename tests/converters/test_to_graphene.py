import pydantic
import graphene
import pydantic2graphene


class Human(pydantic.BaseModel):
    name: str


class TestToGraphene:
    def test_returns_object_type_schema(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(Human, graphene.ObjectType)
        expected_value = """
            type HumanGql {
                name: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_when_graphene_type_is_not_set_use_object_type_as_default(
        self, normalize_sdl,
    ):
        value = pydantic2graphene.to_graphene(Human)
        expected_value = """
            type HumanGql {
                name: String!
            }
        """
        assert normalize_sdl(value) == normalize_sdl(expected_value)
