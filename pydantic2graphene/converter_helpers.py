import typing
import graphene
import pydantic
import inspect

from . import errors
from . import fields
from . import converter
from . import types

ToGrapheneOptions = converter.ToGrapheneOptions


def to_graphene(
    pydantic_model: pydantic.BaseModel,
    graphene_type: types.GrapheneObjectType = graphene.ObjectType,
    options: typing.Union[ToGrapheneOptions, dict] = None,
) -> types.GrapheneObjectType:
    return converter.ToGraphene(
        pydantic_model, graphene_type, options
    ).convert()


class ConverterToGrapheneBase:
    @classmethod
    def as_class(
        cls, graphene_type: types.GrapheneObjectType = None
    ) -> types.GrapheneObjectType:
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
            if fields.is_graphene_type(value)
        }

        params = {
            "pydantic_model": model,
            "options": options,
        }
        graphene_type = graphene_type or getattr(Config, "graphene_type", None)
        if graphene_type:
            params["graphene_type"] = graphene_type

        return to_graphene(**params)
