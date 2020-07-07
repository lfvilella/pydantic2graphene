__all__ = [
    "ToGrapheneOptions",
    "to_graphene",
    "ConverterToGrapheneBase",
]

import typing
import logging
import graphene
import pydantic
import inspect

from . import errors
from . import fields


def _get_field_by_type(pydantic_field: pydantic.fields.ModelField):
    type_ = pydantic_field.type_
    type_args = getattr(type_, "__args__", [])

    if pydantic_field.shape in fields.LIST_SHAPES and len(type_args):
        type_ = type_args[0]
        if len(type_args) > 1:
            logging.warn(
                "%s, has multiple only the first type was used",
                pydantic_field.name,
            )

    field = fields.get_grapehene_field_by_type(type_)
    if field:
        return field

    if type_ in fields.LIST_FIELDS_NOT_TYPED:
        raise errors.InvalidListType(
            "Lists must be type, e.g typing.List[int]"
        )

    if inspect.isclass(type_) and issubclass(type_, fields.ENUM_TYPE):
        return graphene.Enum.from_enum(type_)

    if inspect.isclass(type_) and issubclass(type_, pydantic.BaseModel):
        return to_graphene(type_)


def _get_graphene_field(pydantic_field: pydantic.fields.ModelField):

    if pydantic_field.shape in fields.NOT_SUPPORTED_SHAPES:
        raise errors.FieldNotSupported(pydantic_field.name)

    args = {
        "required": pydantic_field.required,
        "default_value": pydantic_field.default,
    }
    field = _get_field_by_type(pydantic_field)
    if not field:
        raise errors.FieldNotSupported(pydantic_field.name)

    if pydantic_field.shape in fields.LIST_SHAPES:
        if pydantic_field.required:
            return graphene.List(graphene.NonNull(field), **args)
        return graphene.List(field, **args)

    return graphene.Field(field, **args)


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


def _generate_class_name(
    pydantic_model: pydantic.BaseModel,
    graphene_type: fields.graphene_type = graphene.ObjectType,
):
    _name = _get_pydantic_class_name(pydantic_model)

    if issubclass(graphene_type, graphene.InputObjectType):
        return f"{_name}InputGql"

    if issubclass(graphene_type, graphene.Interface):
        return f"{_name}InterfaceGql"

    return f"{_name}Gql"


class ToGrapheneOptions(pydantic.BaseModel):
    id_field_name: str = None

    extra_fields: typing.Mapping[
        str, typing.TypeVar("graphene.BaseType"),
    ] = pydantic.Field(default_factory=dict)

    exclude_fields: typing.Set[str] = pydantic.Field(default_factory=set)

    class_name: str = None

    @pydantic.validator("extra_fields")
    def validate_extra_fields(cls, value):
        if not value:
            return value

        for k, v in value.items():
            if "graphene.types" not in repr(v):
                raise errors.InvalidType(
                    f'Invalid field "{k}", is not a graphene filed'
                )

        return value


def to_graphene(
    pydantic_model: pydantic.BaseModel,
    graphene_type: fields.graphene_type = graphene.ObjectType,
    options: typing.Union[ToGrapheneOptions, dict] = None,
) -> fields.graphene_type:

    options = options or {}
    if not isinstance(options, ToGrapheneOptions):
        options = ToGrapheneOptions(**options)

    graphene_attrs = {}
    for field in _get_pydantic_fields(pydantic_model):
        if field.name in options.extra_fields:
            continue

        if field.name in options.exclude_fields:
            continue

        graphene_attrs[field.name] = _get_graphene_field(field)

    graphene_attrs.update(options.extra_fields)

    if options.id_field_name:
        graphene_attrs[options.id_field_name] = graphene.ID(required=True)

    class_name = options.class_name or _generate_class_name(
        pydantic_model, graphene_type
    )

    graphene_class = type(class_name, (graphene_type,), graphene_attrs)
    return graphene_class


class ConverterToGrapheneBase:
    @classmethod
    def as_class(
        cls, graphene_type: fields.graphene_type = None
    ) -> fields.graphene_type:
        Config = getattr(cls, "Config", None)
        if not inspect.isclass(Config):
            raise errors.InvalidConfigClass("Config is invalid")

        model = getattr(Config, "model", None)
        if not model:
            raise errors.InvalidConfigClass(
                'Config is missing "model" property'
            )

        options = {k: v for k, v in vars(Config).items()}
        options["extra_fields"] = {
            attr: value
            for attr, value in vars(cls).items()
            if "graphene.types" in repr(value)
        }

        params = {
            "pydantic_model": model,
            "options": options,
        }
        graphene_type = graphene_type or getattr(Config, "graphene_type", None)
        if graphene_type:
            params["graphene_type"] = graphene_type

        return to_graphene(**params)
