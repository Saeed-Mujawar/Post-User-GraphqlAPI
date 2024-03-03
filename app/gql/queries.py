from graphene import ObjectType
from app.gql.post.query import PostQuery
from app.gql.user.query import UserQuery 

class Query(PostQuery, UserQuery, ObjectType):
    pass


 
