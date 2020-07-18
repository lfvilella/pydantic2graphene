import collections
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
    obj: typing.Union[
        str, graphene.ObjectType, graphene.InputObjectType, graphene.Interface
    ],
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


@pytest.fixture
def module_wrapper():
    class ModuleWrapper:
        def __init__(self, module, exclude=None, force_exception=None):
            self.module = module
            self.exclude = set(exclude or [])
            self.called_count = collections.Counter()
            self.exceptions = collections.Counter()
            self.force_exception = force_exception or {}

        def __getattribute__(self, attr):
            _self = super().__getattribute__("__dict__")
            if attr in _self:
                return _self[attr]

            _self["called_count"][attr] += 1
            if attr in _self["exclude"]:
                _self["exceptions"][attr] += 1
                raise AttributeError

            if attr in _self["force_exception"]:
                _self["exceptions"][attr] += 1
                raise _self["force_exception"][attr]

            return getattr(_self["module"], attr)

    return ModuleWrapper
