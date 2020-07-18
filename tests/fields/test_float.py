import graphene
import pydantic
import pydantic2graphene


class MyModel(pydantic.BaseModel):
    field1: float
    field2: float = 3.14159265359


def test_schema_type_declaration(normalize_sdl):
    value = pydantic2graphene.to_graphene(MyModel)
    expected_value = """
        type MyModelGql {
            field1: Float!
            field2: Float
        }
    """
    assert normalize_sdl(value) == normalize_sdl(expected_value)


def test_schema_input_declaration(normalize_sdl):
    value = pydantic2graphene.to_graphene(MyModel, graphene.InputObjectType)
    expected_value = """
        input MyModelInputGql {
            field1: Float!
            field2: Float=3.14159265359
        }
    """
    assert normalize_sdl(value) == normalize_sdl(expected_value)


def test_schema_interface_declaration(normalize_sdl):
    value = pydantic2graphene.to_graphene(MyModel, graphene.Interface)
    expected_value = """
        interface MyModelInterfaceGql {
            field1: Float!
            field2: Float
        }
        type Query implements MyModelInterfaceGql {
            field1: Float!
            field2: Float
        }
    """
    assert normalize_sdl(value) == normalize_sdl(expected_value)


def test_query_usage(simple_query_schema):
    MyModelGql = pydantic2graphene.to_graphene(MyModel)
    schema = simple_query_schema(MyModelGql, MyModel(field1=10, field2=20))

    query = """
    query {
        hello {
            f1: field1
            field2
        }
    }
    """
    value = schema.execute(query).data
    expected_value = {"hello": {"f1": 10, "field2": 20}}

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
        h1: hello (inp: {field1: 99.01}) {
            f1: field1
            f2: field2
        }

        h2: hello (inp: {field1: 109.01, field2: 101.1}) {
            field1
            field2
        }
    }
    """
    value = schema.execute(query).data
    expected_value = {
        "h1": {"f1": 99.01, "f2": 3.14159265359},
        "h2": {"field1": 109.01, "field2": 101.1},
    }

    assert value == expected_value
