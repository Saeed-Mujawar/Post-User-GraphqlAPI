from graphene import ObjectType, String, Int, List, Field, Boolean

class UserObject(ObjectType):
    id = Int()
    username = String()
    email = String()
    # otp = String()  
    # email_verified = Boolean()
    posts = List(lambda: PostObject)

    @staticmethod
    def resolve_posts(root, info):
        return root.posts
    
class PostObject(ObjectType):
    id = Int()
    title = String()
    body = String()
    user_id = Int()
    user = Field(lambda: UserObject)

    @staticmethod
    def resolve_user(root, info):
        return root.user

    
    