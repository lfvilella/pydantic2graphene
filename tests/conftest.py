import typing
import pytest
import graphene


def _get_type_sdl(obj):
    sdl = str(graphene.Schema(query=obj))
    return sdl.split("}", 1)[1].strip()


def _get_input_sdl(obj):
    class Query(graphene.ObjectType):
        foo = graphene.String(node=obj())

    sdl = str(graphene.Schema(query=Query))
    return sdl.split("}", 1)[1].split("type")[0].strip()


def _get_interface_sdl(obj):
    class Query(graphene.ObjectType):
        class Meta:
            interfaces = (obj,)

    sdl = str(graphene.Schema(query=Query))
    return sdl.split("}", 1)[1].strip()


def obj_to_sdl(
    obj: typing.Union[str, graphene.ObjectType, graphene.InputObjectType, graphene.Interface],
) -> str:
    if isinstance(obj, str):
        return obj

    if issubclass(obj, graphene.ObjectType):
        return _get_type_sdl(obj)

    if issubclass(obj, graphene.InputObjectType):
        return _get_input_sdl(obj)

    if issubclass(obj, graphene.Interface):
        return _get_interface_sdl(obj)

    raise ValueError("Invalid Schema Definition Language (SDL) type")


@pytest.fixture
def get_sdl():
    return obj_to_sdl


@pytest.fixture
def normalize_sdl(get_sdl):
    def _normalize(sdl):
        return "".join(get_sdl(sdl).split())

    return _normalize
