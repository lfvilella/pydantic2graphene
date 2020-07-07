import datetime
import typing
import ipaddress
import enum
import decimal
import uuid

import graphene
import graphene.types.datetime
import pydantic.fields

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

_TYPE_MAPPING = None

def _get_type_mapping():
    global _TYPE_MAPPING
    if _TYPE_MAPPING:
        return _TYPE_MAPPING

    _TYPE_MAPPING = {
        str: graphene.String,
        bool: graphene.Boolean,
        float: graphene.Float,
        int: graphene.Int,
        bytes: graphene.String,
        datetime.datetime: graphene.types.datetime.DateTime,
        typing.Pattern: graphene.String,
        ipaddress.IPv4Address: graphene.String,
        ipaddress.IPv4Interface: graphene.String,
        ipaddress.IPv4Network: graphene.String,
        ipaddress.IPv6Address: graphene.String,
        ipaddress.IPv6Interface: graphene.String,
        ipaddress.IPv6Network: graphene.String,
        decimal.Decimal: graphene.Float,
        uuid.UUID: graphene.String,
        pydantic.EmailStr: graphene.String,
        pydantic.NameEmail: graphene.String,
        pydantic.color.Color: graphene.String,
    }

    # graphene does not support Date on versions:
    # ('1.X', '2.0')
    try:
        _TYPE_MAPPING[datetime.date] = graphene.types.datetime.Date
    except AttributeError:
        pass

    # graphene does not support Time on versions:
    # ('1.1.2', '1.1.1', '1.1', '1.0.2', '1.0.1', '1.0')
    try:
        _TYPE_MAPPING[datetime.time] = graphene.types.datetime.Time
    except AttributeError:
        pass

    # pydantic needs 'email-validator' to this fields
    try:
        _TYPE_MAPPING[pydantic.EmailStr] = graphene.String
        _TYPE_MAPPING[pydantic.NameEmail] = graphene.String
    except ImportError:
        pass

    return _TYPE_MAPPING


def get_grapehene_field_by_type(type_):
    return _get_type_mapping().get(type_)


LIST_FIELDS_NOT_TYPED = {
    list,
    tuple,
    dict,
    set,
    frozenset,
}


ENUM_TYPE = (
    enum.Enum,
    enum.IntEnum,
)

graphene_type = typing.Union[
    graphene.ObjectType, graphene.InputObjectType, graphene.Interface,
]
