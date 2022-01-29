import graphene
import pytest


@pytest.fixture
def simple_query_schema():
    def _get_schema(graphene_object, resolve_return=None):
        class Query(graphene.ObjectType):
            hello = graphene.Field(graphene_object)

            @staticmethod
            def resolve_hello(*args, **kwargs):
                return resolve_return

        schema = graphene.Schema(query=Query)

        return schema

    return _get_schema


@pytest.fixture
def input_query_schema():
    def _get_schema(
        graphene_object,
        graphene_input,
        resolve_return=None,
        resolve_model=None,
    ):
        class Query(graphene.ObjectType):
            hello = graphene.Field(graphene_object, inp=graphene_input)

            @staticmethod
            def resolve_hello(*args, **kwargs):
                if resolve_return:
                    return resolve_return

                inp = kwargs.get("inp") or args[1].get("inp")
                return resolve_model(**inp)

        schema = graphene.Schema(query=Query)
        return schema

    return _get_schema
