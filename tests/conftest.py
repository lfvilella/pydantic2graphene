import collections
import typing
import pytest
import pydantic
import graphene
import re


def _get_type_sdl(obj):
    sdl = str(graphene.Schema(query=obj))
    return sdl.split("}", 1)[1].strip()


def _get_input_sdl(obj):
    class Query(graphene.ObjectType):
        foo = graphene.String(node=obj())

    sdl = str(graphene.Schema(query=Query))
    return re.sub("type Query[^}]*}", "", sdl.split("}", 1)[1].strip())


def _get_interface_sdl(obj):
    class Query(graphene.ObjectType):
        class Meta:
            interfaces = (obj,)

    sdl = str(graphene.Schema(query=Query))
    return re.sub("type Query[^}]*}", "", sdl.split("}", 1)[1].strip())


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
    class WrapperState:
        def __init__(self, module, exclude=None, force_exception=None):
            self.module = module
            self.exclude = set(exclude or [])
            self.called_counter = collections.Counter()
            self.exceptions_counter = collections.Counter()
            self.force_exception = force_exception or {}

    class ModuleWrapper:
        def __init__(self, module, exclude=None, force_exception=None):
            self.wrapper_local_state = WrapperState(
                module, exclude, force_exception
            )

        def __getattribute__(self, attr):
            _self = super().__getattribute__("__dict__")
            if attr in _self:
                return _self[attr]

            _local_state = _self["wrapper_local_state"]

            _local_state.called_counter[attr] += 1
            if attr in _local_state.exclude:
                _local_state.exceptions_counter[attr] += 1
                raise AttributeError

            if attr in _local_state.force_exception:
                _local_state.exceptions_counter[attr] += 1
                raise _local_state.force_exception[attr]

            return getattr(_local_state.module, attr)

    return ModuleWrapper


@pytest.fixture
def graphene_version() -> str:
    return graphene.__version__


@pytest.fixture
def is_graphene_1_or_2(graphene_version) -> bool:
    return graphene_version[:2] in ["1.", "2."]


@pytest.fixture
def pydantic_version() -> str:
    return str(pydantic.VERSION)
