# pydantic2graphene

[![CI](https://github.com/lfvilella/pydantic2graphene/workflows/CI/badge.svg?event=push)](https://github.com/lfvilella/pydantic2graphene/actions?query=event%3Apush+branch%3Amaster+workflow%3ACI)
[![license](https://img.shields.io/github/license/lfvilella/pydantic2graphene.svg)](https://github.com/lfvilella/pydantic2graphene/blob/master/LICENSE)

Easy way to convert pydantic2graphene models to graphene objects.


## A Simple Example

```py
>>> import graphene
>>> import pydantic
>>> import pydantic2graphene
>>> 
>>> class User(pydantic.BaseModel):
...     email: str
...     active: bool = False
... 
>>> UserGql = pydantic2graphene.to_graphene(User)
>>> 
>>> class Query(graphene.ObjectType):
...     all_users = graphene.List(UserGql)
...     @staticmethod
...     def resolve_all_users(parent, info):
...         return [
...             {'email': 'my-email@localhost.com', 'active': True},
...             User(email='email@localhost.com', active=False),
...         ]
... 
>>> schema = graphene.Schema(query=Query)
>>> print(schema)
schema {
  query: Query
}

type Query {
  allUsers: [UserGql]
}

type UserGql {
  email: String!
  active: Boolean
}

>>> command = '''
... query {
...     emailOnly: allUsers {
...         email
...     }
... 
...     all: allUsers {
...         isActive: active
...         email
...     }
... }
... '''
>>>
>>> print(schema.execute(command))
{
    'data': {
        'emailOnly': [
            {'email': 'my-email@localhost.com'},
            {'email': 'email@localhost.com'}
        ],
        'all': [
            {'isActive': True, 'email': 'my-email@localhost.com'}, 
            {'isActive': False, 'email': 'email@localhost.com'}
        ]
    }
}
```
