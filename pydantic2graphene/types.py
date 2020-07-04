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
}

TYPE_MAPPING = {
    str: graphene.String,
    bool: graphene.Boolean,
    float: graphene.Float,
    int: graphene.Int,
    bytes: graphene.String,
    list: graphene.List(graphene.String),
    # tuple: None,
    # dict: None,
    # set: None,
    # frozenset: None,
    datetime.date: graphene.types.datetime.Date,
    datetime.datetime: graphene.types.datetime.DateTime,
    datetime.time: graphene.types.datetime.Time,
    # datetime.timedelta: None,
}

graphene_type = typing.Union[
    graphene.ObjectType, graphene.InputObjectType, graphene.Interface,
]
