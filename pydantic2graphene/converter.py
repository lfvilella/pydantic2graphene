import typing
import logging
import graphene
import pydantic
import inspect

from . import errors
from . import fields
from . import types

_module_cache = {}


def _get_pydantic_class_name(pydantic_model: pydantic.BaseModel) -> str:
    """
    >>> str(Human)
    "<class 'api.Human'>"
    """
    return str(pydantic_model).split("'")[1].split(".")[-1]


def _get_pydantic_fields(
    pydantic_model: pydantic.BaseModel,
) -> typing.List[pydantic.fields.ModelField]:
    """
    >>> str(Human)
    "<class 'api.Human'>"
    """
    return pydantic_model.__fields__.values()


class ToGrapheneOptions(pydantic.BaseModel):
    id_field_name: str = None

    extra_fields: typing.Mapping[str, types.GrapheneField] = {}

    exclude_fields: typing.Set[str] = set()

    class_name: str = None

    use_cache: bool = True

    @pydantic.validator("extra_fields")
    def validate_extra_fields(cls, value):
        if not value:
            return value

        for k, v in value.items():
            if not fields.is_graphene_type(v):
                raise errors.InvalidType(
                    f'Invalid field "{k}", is not a graphene filed'
                )

        return value


class ToGraphene:
    _cache: dict
    options: ToGrapheneOptions
    pydantic_model: pydantic.BaseModel
    graphene_type: types.GrapheneObjectType

    def __init__(
        self: object,
        pydantic_model: pydantic.BaseModel,
        graphene_type: types.GrapheneObjectType = graphene.ObjectType,
        options: typing.Union[ToGrapheneOptions, dict] = None,
        cache: dict = None,
    ):
        options = options or {}
        if not isinstance(options, ToGrapheneOptions):
            options = ToGrapheneOptions(**options)

        self.options = options
        self.pydantic_model = pydantic_model
        self.graphene_type = graphene_type
        self._cache = cache or _module_cache

    def _get_from_cache(
        self,
        pydantic_model: pydantic.BaseModel,
        graphene_type: types.GrapheneObjectType = graphene.ObjectType,
    ) -> types.GrapheneObjectType:
        cache_key = (pydantic_model, graphene_type)
        if not inspect.isclass(pydantic_model):  # when instance get the class
            cache_key = (pydantic_model.__class__, graphene_type)

        if self.options.use_cache and cache_key in self._cache:
            return (cache_key, self._cache[cache_key])

        return (cache_key, None)

    def _generate_class_name(self):
        _name = _get_pydantic_class_name(self.pydantic_model)

        if issubclass(self.graphene_type, graphene.InputObjectType):
            return f"{_name}InputGql"

        if issubclass(self.graphene_type, graphene.Interface):
            return f"{_name}InterfaceGql"

        return f"{_name}Gql"

    def _convert_to_graphene_field(
        self, pydantic_field: pydantic.fields.ModelField
    ):
        shape = pydantic_field.shape
        if fields.is_not_supported_shape(shape):
            raise errors.FieldNotSupported(pydantic_field.name)

        type_ = pydantic_field.type_
        type_args = getattr(type_, "__args__", [])

        if fields.is_list_shape(shape) and len(type_args):
            type_ = type_args[0]
            if len(type_args) > 1:
                logging.warn(
                    "%s, has multiple only the first type was used",
                    pydantic_field.name,
                )

        if fields.is_enum_type(type_):
            cache_key, cached_obj = self._get_from_cache(type_, graphene.Enum)
            if cached_obj:
                return cached_obj

            graphene_enum = graphene.Enum.from_enum(type_)
            self._cache[cache_key] = graphene_enum
            return graphene_enum

        if fields.is_pydantic_base_model(type_):
            if self.graphene_type == graphene.InputObjectType:
                obj_type = self.graphene_type
            else:
                obj_type = graphene.ObjectType

            return ToGraphene(type_, obj_type).convert()

        field = fields.get_grapehene_field_by_type(type_)
        if field:
            return field

        if fields.is_field_not_allowed_type(type_):
            raise errors.InvalidListType(
                "Lists must be type, e.g typing.List[int]"
            )

        outer_type_ = getattr(pydantic_field, "outer_type_", None)
        if outer_type_:
            field_outer = fields.get_grapehene_field_by_type(outer_type_)
            if field_outer:
                return field_outer

    def _get_graphene_field(self, pydantic_field: pydantic.fields.ModelField):
        args = {
            "required": pydantic_field.required,
            "default_value": pydantic_field.default,
        }
        field = self._convert_to_graphene_field(pydantic_field)
        if not field:
            raise errors.FieldNotSupported(pydantic_field.name)

        if fields.is_list_shape(pydantic_field.shape):
            if pydantic_field.required:
                return graphene.List(graphene.NonNull(field), **args)
            return graphene.List(field, **args)

        return graphene.Field(field, **args)

    def convert(self) -> types.GrapheneObjectType:

        cache_key, cached_obj = self._get_from_cache(
            self.pydantic_model, self.graphene_type
        )
        if cached_obj:
            return cached_obj

        graphene_attrs = {}
        for field in _get_pydantic_fields(self.pydantic_model):
            if field.name in self.options.extra_fields:
                continue

            if field.name in self.options.exclude_fields:
                continue

            graphene_attrs[field.name] = self._get_graphene_field(field)

        graphene_attrs.update(self.options.extra_fields)

        if self.options.id_field_name:
            graphene_attrs[self.options.id_field_name] = graphene.ID(
                required=True
            )

        class_name = self.options.class_name or self._generate_class_name()

        GrapheneClass = type(class_name, (self.graphene_type,), graphene_attrs)

        self._cache[cache_key] = GrapheneClass
        return GrapheneClass
