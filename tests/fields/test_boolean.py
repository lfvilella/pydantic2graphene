import graphene
import pydantic
import pydantic2graphene


class MyModel(pydantic.BaseModel):
    field1: bool
    field2: bool = True
    field3: bool = False


def test_schema_type_declaration(normalize_sdl):
    value = pydantic2graphene.to_graphene(MyModel)
    expected_value = """
        type MyModelGql {
            field1: Boolean!
            field2: Boolean
            field3: Boolean
        }
    """
    assert normalize_sdl(value) == normalize_sdl(expected_value)


def test_schema_input_declaration(normalize_sdl):
    value = pydantic2graphene.to_graphene(MyModel, graphene.InputObjectType)
    expected_value = """
        input MyModelInputGql {
            field1: Boolean!
            field2: Boolean = true
            field3: Boolean = false
        }
    """
    assert normalize_sdl(value) == normalize_sdl(expected_value)


def test_schema_interface_declaration(normalize_sdl):
    value = pydantic2graphene.to_graphene(MyModel, graphene.Interface)
    expected_value = """
        interface MyModelInterfaceGql {
            field1: Boolean!
            field2: Boolean
            field3: Boolean
        }
        type Query implements MyModelInterfaceGql {
            field1: Boolean!
            field2: Boolean
            field3: Boolean
        }
    """
    assert normalize_sdl(value) == normalize_sdl(expected_value)


def test_query_usage(simple_query_schema):
    MyModelGql = pydantic2graphene.to_graphene(MyModel)
    schema = simple_query_schema(
        MyModelGql, MyModel(field1=True, field2=True, field3=False)
    )

    query = """
    query {
        hello {
            f1: field1
            field2
            f3: field3
        }
    }
    """
    value = schema.execute(query).data
    expected_value = {"hello": {"f1": True, "field2": True, "f3": False}}

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
        h1: hello (inp: {field1: true}) {
            f1: field1
            f2: field2
        }

        h2: hello (inp: {field1: false, field2: false, field3: true}) {
            field1
            field2
            field3
        }
    }
    """
    value = schema.execute(query).data
    expected_value = {
        "h1": {"f1": True, "f2": True},
        "h2": {"field1": False, "field2": False, "field3": True},
    }

    assert value == expected_value
