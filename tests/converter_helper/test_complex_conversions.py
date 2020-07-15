import datetime
import enum
import typing

import pydantic
import graphene
import pydantic2graphene


class SpecieEnum(str, enum.Enum):
    DOG = "DOG"
    CAT = "CAT"
    OTHER = "OTHER"


class Pet(pydantic.BaseModel):
    name: str
    specie: SpecieEnum


class Human(pydantic.BaseModel):
    name: str
    birth_date: datetime.datetime
    pets: typing.List[Pet] = pydantic.Field(default_factory=list)


class TestConvertingComplexModels:
    def test_returns_object_type_schema(self, normalize_sdl):
        value = pydantic2graphene.to_graphene(Human, graphene.ObjectType)
        expected_value = """
            scalar DateTime

            type HumanGql {
                name: String!
                birthDate: DateTime!
                pets: [PetGql]
            }

            type PetGql {
                name: String!
                specie: SpecieEnum!
            }

            enum SpecieEnum {
                DOG
                CAT
                OTHER
            }
        """

        # version_1_6 = pydantic.VERSION.startswith("1.6")
        # if version_1_6:
        #     expected_value = '''
        #         type HumanGql {
        #             name: String!
        #             birthDate: DateTime!
        #             pets: [PetGql]
        #         }

        #         """
        #         The `DateTime` scalar type represents a DateTime
        #         value as specified by
        #         [iso8601](https://en.wikipedia.org/wiki/ISO_8601).
        #         """
        #         scalar DateTime

        #         type PetGql {
        #             name: String!
        #             specie: SpecieEnum!
        #         }

        #         """An enumeration."""
        #         enum SpecieEnum {
        #             DOG
        #             CAT
        #             OTHER
        #         }
        #     '''

        assert normalize_sdl(value) == normalize_sdl(expected_value)

    def test_create_query_schema(self, normalize_sdl):
        HumanGql = pydantic2graphene.to_graphene(Human)
        PetGql = pydantic2graphene.to_graphene(Pet)
        PetInputGql = pydantic2graphene.to_graphene(
            Pet, graphene.InputObjectType
        )

        class Query(graphene.ObjectType):
            all_humans = graphene.List(HumanGql)
            filter_pets = graphene.List(PetGql, filter=PetInputGql())

        value = Query
        expected_value = """
            scalar DateTime

            type HumanGql {
                name: String!
                birthDate: DateTime!
                pets: [PetGql]
            }

            type PetGql {
                name: String!
                specie: SpecieEnum!
            }

            input PetInputGql {
                name: String!
                specie: SpecieEnum!
            }

            type Query {
                allHumans: [HumanGql]
                filterPets(filter: PetInputGql): [PetGql]
            }

            enum SpecieEnum {
                DOG
                CAT
                OTHER
            }
        """

        # version_1_6 = pydantic.VERSION.startswith("1.6")
        # if version_1_6:
        #     expected_value = '''
        #         type HumanGql {
        #             name: String!
        #             birthDate: DateTime!
        #             pets: [PetGql]
        #         }

        #         """
        #         The `DateTime` scalar type represents a DateTime
        #         value as specified by
        #         [iso8601](https://en.wikipedia.org/wiki/ISO_8601).
        #         """
        #         scalar DateTime

        #         type PetGql {
        #             name: String!
        #             specie: SpecieEnum!
        #         }

        #         """An enumeration."""
        #         enum SpecieEnum {
        #             DOG
        #             CAT
        #             OTHER
        #         }

        #         input PetInputGql {
        #             name: String!
        #             specie: SpecieEnum!
        #         }
        #     '''
        assert normalize_sdl(value) == normalize_sdl(expected_value)
