from graphene import ObjectType 
from app.gql.post.mutation import AddPost, DeletePost, UpdatePost
from app.gql.user.mutation import AddUser, DeleteUser, UpdateUser, LoginUser


# By adding these mutation fields to the Mutation class, you're effectively exposing them 
#     in your GraphQL schema, making them accessible to clients through GraphQL queries.
class Mutation(ObjectType):
    add_post = AddPost.Field()
    delete_post = DeletePost.Field()
    update_post = UpdatePost.Field()

    add_user = AddUser.Field()
    delete_user = DeleteUser.Field()
    update_user = UpdateUser.Field()
    login_user = LoginUser.Field()
    # verify_otp = VerifyOTP.Field()

