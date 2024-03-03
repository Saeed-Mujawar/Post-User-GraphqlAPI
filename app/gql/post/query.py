from graphene import ObjectType, List, Field, Int
from app.gql.schemas import PostObject
from app.db.database import Session
from app.db.models import Post


class PostQuery(ObjectType):
    posts = List(PostObject)
    post = Field(PostObject, post_id=Int(required=True))

    @staticmethod
    def resolve_posts(root, info):
        return Session().query(Post).all()

    @staticmethod
    def resolve_post(root, info, post_id):
        return Session().query(Post).filter(Post.id == post_id).first()
