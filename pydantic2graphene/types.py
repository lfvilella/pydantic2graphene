import typing
import graphene
import pydantic
import datetime


NOT_SUPPORTED_SHAPES = {
    pydantic.fields.SHAPE_MAPPING,
}

LIST_SHAPES = {
    pydantic.fields.SHAPE_LIST,
    pydantic.fields.SHAPE_TUPLE,
    pydantic.fields.SHAPE_TUPLE_ELLIPSIS,
    pydantic.fields.SHAPE_SEQUENCE,
    pydantic.fields.SHAPE_SET,
    pydantic.fields.SHAPE_FROZENSET,
    pydantic.fields.SHAPE_ITERABLE,
}

TYPE_MAPPING = {
    str: graphene.String,
    bool: graphene.Boolean,
    float: graphene.Float,
    int: graphene.Int,
    bytes: graphene.String,
    datetime.date: graphene.types.datetime.Date,
    datetime.datetime: graphene.types.datetime.DateTime,
    datetime.time: graphene.types.datetime.Time,
}

LIST_FIELDS_NOT_TYPED = {
    list,
    tuple,
    dict,
    set,
    frozenset,
}

graphene_type = typing.Union[
    graphene.ObjectType, graphene.InputObjectType, graphene.Interface,
]
