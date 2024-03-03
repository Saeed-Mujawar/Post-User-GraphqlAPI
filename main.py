from graphene import Schema
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_playground_handler 
from app.db. models import Base
from app.db.database import engine
from app. gql.queries import Query
from app.gql.mutations import Mutation


schema = Schema(query=Query, mutation= Mutation)

app = FastAPI()


@app.on_event("startup")
def startup_event():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    # prepare_database()

app.mount("/", GraphQLApp(
    schema=schema,
    on_get = make_playground_handler()
    ))


