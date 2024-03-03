from graphene import ObjectType, List, Field, Int
from app.gql.schemas import UserObject
from app.db.database import Session
from app.db.models import User

class UserQuery(ObjectType):
    users = List(UserObject)
    user = Field(UserObject, user_id=Int(required=True))

    @staticmethod
    def resolve_users(root, info):
        return Session().query(User).all()

    @staticmethod
    def resolve_user(root, info, user_id):
        return Session().query(User).filter(User.id == user_id).first()
