import graphene
import pydantic
import pydantic2graphene


class MyModel(pydantic.BaseModel):
    field1: str
    field2: str = "abc"


def test_schema_type_declaration(normalize_sdl):
    value = pydantic2graphene.to_graphene(MyModel)
    expected_value = """
        type MyModelGql {
            field1: String!
            field2: String
        }
    """
    assert normalize_sdl(value) == normalize_sdl(expected_value)


def test_schema_input_declaration(normalize_sdl):
    value = pydantic2graphene.to_graphene(MyModel, graphene.InputObjectType)
    expected_value = """
        input MyModelInputGql {
            field1: String!
            field2: String="abc"
        }
    """
    assert normalize_sdl(value) == normalize_sdl(expected_value)


def test_schema_interface_declaration(normalize_sdl):
    value = pydantic2graphene.to_graphene(MyModel, graphene.Interface)
    expected_value = """
        interface MyModelInterfaceGql {
            field1: String!
            field2: String
        }
    """
    assert normalize_sdl(value) == normalize_sdl(expected_value)


def test_query_usage(simple_query_schema):
    MyModelGql = pydantic2graphene.to_graphene(MyModel)
    schema = simple_query_schema(
        MyModelGql, MyModel(field1="lets", field2="rock")
    )
    query = """
    query {
        hello {
            f1: field1
            field2
        }
    }
    """
    value = schema.execute(query).data
    expected_value = {"hello": {"f1": "lets", "field2": "rock"}}

    assert value == expected_value


def test_input_usage(input_query_schema):
    MyModelGql = pydantic2graphene.to_graphene(MyModel)
    MyModelInputGql = pydantic2graphene.to_graphene(
        MyModel, graphene.InputObjectType
    )

    schema = input_query_schema(
        MyModelGql, MyModelInputGql(), resolve_model=MyModel
    )

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
    value = schema.execute(query).data
    expected_value = {
        "h1": {"f1": "123", "f2": "abc"},
        "h2": {"field1": "go", "field2": "python"},
    }

    assert value == expected_value
