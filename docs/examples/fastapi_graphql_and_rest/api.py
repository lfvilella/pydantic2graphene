import typing
import uuid

import fastapi
import graphene
import pydantic
import starlette.graphql

import pydantic2graphene

app = fastapi.FastAPI()


###############################
#          Schema             #
###############################


class CamelBaseModel(pydantic.BaseModel):
    class Config:
        def _camel(obj: str) -> str:
            _str = "".join(map(str.capitalize, obj.split("_")))
            return _str[0].lower() + _str[1:]

        alias_generator = _camel
        allow_population_by_field_name = True


class Item(CamelBaseModel):
    name: str
    price: float
    is_offer: bool = False


class ItemDB(Item):
    id: uuid.UUID


class ItemFilter(CamelBaseModel):
    name: str = None
    is_offer: bool = None


###############################
#         Data Access         #
###############################

_ALL_ITEMS: typing.List[ItemDB] = [
    ItemDB(
        id="d19c0e72-3a4e-4256-aa46-d6262ea65523",
        name="beer",
        price=2.0,
        is_offer=False,
    ),
    ItemDB(
        id="40293edb-52ca-4a3b-9973-b6cb3ea11d2c",
        name="cake",
        price=10.0,
        is_offer=True,
    ),
    ItemDB(
        id="86428e49-46bb-4295-bfa7-4eb3d277ad9d",
        name="pizza",
        price=4.0,
        is_offer=False,
    ),
]


def filter_items(filters: ItemFilter) -> typing.List[ItemDB]:
    items = []

    for item in _ALL_ITEMS:
        if filters.name is not None and item.name != filters.name:
            continue

        if filters.is_offer is not None and item.is_offer != filters.is_offer:
            continue

        items.append(item)

    return items


def create_item(item: Item) -> ItemDB:
    item_db = ItemDB(id=uuid.uuid4(), **item.dict())
    _ALL_ITEMS.append(item_db)
    return item_db


###############################
#          REST API           #
###############################


@app.get("/items", response_model=typing.List[ItemDB])
def items_filter(q: ItemFilter = fastapi.Depends(ItemFilter)):
    return filter_items(q)


@app.post("/items", status_code=201, response_model=ItemDB)
def items_create(item: Item):
    return create_item(item)


###############################
#           GraphQL           #
###############################

ItemDBGql = pydantic2graphene.to_graphene(
    ItemDB, options={"id_field_name": "id"}
)
ItemFilterInputGql = pydantic2graphene.to_graphene(
    ItemFilter, graphene.InputObjectType
)

ItemInputGql = pydantic2graphene.to_graphene(Item, graphene.InputObjectType)


class Query(graphene.ObjectType):
    filter_items = graphene.List(ItemDBGql, filters=ItemFilterInputGql())

    @staticmethod
    def resolve_filter_items(parent, info, filters):
        return filter_items(ItemFilter(**filters))


class CreateItem(graphene.Mutation):
    class Arguments:
        item = ItemInputGql()

    Output = ItemDBGql

    @staticmethod
    def mutate(parent, info, item):
        return create_item(Item(**item))


class Mutations(graphene.ObjectType):
    create_item = CreateItem.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)

app.add_route("/graphql", starlette.graphql.GraphQLApp(schema=schema))
