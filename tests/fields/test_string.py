import graphene
import pydantic
import pydantic2graphene


class MyModel(pydantic.BaseModel):
    field1: str
    field2: str = "abc"


def test_schema_declaration(normalize_sdl):
    value = pydantic2graphene.to_graphene(MyModel)
    expected_value = """
        type MyModelGql {
            field1: String!
            field2: String
        }
    """
    assert normalize_sdl(value) == normalize_sdl(expected_value)


def test_query_usage():
    MyModelGql = pydantic2graphene.to_graphene(MyModel)

    class Query(graphene.ObjectType):
        hello = graphene.Field(MyModelGql)

        @staticmethod
        def resolve_hello(parent, info):
            return MyModel(field1="lets", field2="rock")

    schema = graphene.Schema(query=Query)

    query = """
    query {
        hello {
            f1: field1
            field2
        }
    }
    """
    value = schema.execute(query).to_dict()
    expected_value = {"data": {"hello": {"f1": "lets", "field2": "rock"}}}

    assert value == expected_value


def test_input_usage():
    MyModelGql = pydantic2graphene.to_graphene(MyModel)
    MyModelInputGql = pydantic2graphene.to_graphene(
        MyModel, graphene.InputObjectType
    )

    class Query(graphene.ObjectType):
        hello = graphene.Field(MyModelGql, inp=MyModelInputGql())

        @staticmethod
        def resolve_hello(parent, info, inp):
            return inp

    schema = graphene.Schema(query=Query)

    query = """
    query {
        h1: hello (inp: {field1: "123"}) {
            f1: field1
            f2: field2
        }

        h2: hello (inp: {field1: "go", field2: "python"}) {
            field1
            field2
        }
    }
    """
    value = schema.execute(query).to_dict()
    expected_value = {
        "data": {
            "h1": {"f1": "123", "f2": "abc"},
            "h2": {"field1": "go", "field2": "python"},
        }
    }

    assert value == expected_value
