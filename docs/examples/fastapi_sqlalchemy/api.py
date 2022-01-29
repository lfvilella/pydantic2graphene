import abc
import contextlib
import os
import typing
import uuid

import fastapi
import graphene
import pydantic
import pydantic_sqlalchemy
import sqlalchemy
import sqlalchemy.ext.declarative
import starlette.graphql

import pydantic2graphene

###############################
#      SQLAlchemy Conf        #
###############################

SQLALCHEMY_DATABASE_URL = os.environ.get(
    "SQLALCHEMY_DATABASE_URL", "sqlite://///tmp/sql_app.db"
)

engine = sqlalchemy.create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sqlalchemy.orm.sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base = sqlalchemy.ext.declarative.declarative_base()


@contextlib.contextmanager
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


###############################
#          Models             #
###############################


class ModelItem(Base):
    __tablename__ = "items"

    @staticmethod
    def generate_id():
        return str(uuid.uuid4())

    id = sqlalchemy.Column(
        sqlalchemy.String,
        primary_key=True,
        unique=True,
        index=True,
        default=generate_id,
    )
    name = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.Float)
    is_offer = sqlalchemy.Column(sqlalchemy.Boolean, default=False)


Base.metadata.create_all(bind=engine)

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


class Item(
    CamelBaseModel,
    pydantic_sqlalchemy.sqlalchemy_to_pydantic(ModelItem, exclude=["id"]),
):
    pass


class ItemDB(Item):
    class Config:
        orm_mode = True

    id: uuid.UUID


class ItemFilter(CamelBaseModel):
    name_equal: str = None
    name_contains: str = None
    is_offer: bool = None


###############################
#         Data Access         #
###############################


class ApplyFilter(metaclass=abc.ABCMeta):
    def __init__(self, model, query, filters: object):
        self.model = model
        self.query = query
        self.filters = filters

    @abc.abstractmethod
    def filter():
        pass


class FilterName(ApplyFilter):
    def filter(self):
        filters: ItemFilter = self.filters
        model: ModelItem = self.model

        q = self.query

        if filters.name_equal is not None:
            q = q.filter(model.name == filters.name_equal)

        if filters.name_contains is not None:
            q = q.filter(model.name.contains(filters.name_contains))

        return q


class FilterOffer(ApplyFilter):
    def filter(self):
        filters: ItemFilter = self.filters
        model: ModelItem = self.model

        q = self.query

        if filters.is_offer is not None:
            q = q.filter(model.is_offer == filters.is_offer)

        return q


class ItemService:
    _session: sqlalchemy.orm.Session = None

    def __init__(self, session: sqlalchemy.orm.Session):
        self._session = session

    def filter_items(self, filters: ItemFilter) -> typing.List[ItemDB]:
        query = self._session.query(ModelItem)
        for FilterClass in ApplyFilter.__subclasses__():
            query = FilterClass(ModelItem, query, filters).filter()

        return list(map(ItemDB.from_orm, query.all()))

    def create_item(self, item: Item, persist: bool = True) -> ItemDB:
        item = ModelItem(id=ModelItem.generate_id(), **item.dict())

        self._session.add(item)
        if persist:
            self._session.commit()
            self._session.flush()

        return ItemDB.from_orm(item)


###############################
#          REST API           #
###############################

app = fastapi.FastAPI()


@app.get("/items", response_model=typing.List[ItemDB])
def items_filter(q: ItemFilter = fastapi.Depends(ItemFilter)):
    with db_session() as session:
        return ItemService(session).filter_items(q)


@app.post("/items", status_code=201, response_model=ItemDB)
def items_create(item: Item):
    with db_session() as session:
        return ItemService(session).create_item(item)


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
        with db_session() as session:
            return ItemService(session).filter_items(ItemFilter(**filters))


class CreateItem(graphene.Mutation):
    class Arguments:
        item = ItemInputGql()

    Output = ItemDBGql

    @staticmethod
    def mutate(parent, info, item):
        with db_session() as session:
            return ItemService(session).create_item(Item(**item))


class Mutations(graphene.ObjectType):
    create_item = CreateItem.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)

app.add_route("/graphql", starlette.graphql.GraphQLApp(schema=schema))
