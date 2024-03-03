from graphene import Mutation, String, Int, Field, Boolean
from app.gql.schemas import PostObject
from app.db.database import Session
from app.db.models import Post
from app.utils import authorize_user_by_id, get_aunthenticated_user


class AddPost(Mutation):
    class Arguments:
        title = String(required = True)
        body = String(required = True)
        user_id = Int(required = True)

    post = Field(lambda: PostObject)

    @authorize_user_by_id
    def mutate(root, info,title,  body, user_id):
        post = Post(title = title , body = body, user_id = user_id)
        session = Session()
        session.add(post)
        session.commit()
        session.refresh(post)

        return AddPost(post=post)

class UpdatePost(Mutation):
    class Arguments:
        post_id = Int(required = True)
        user_id = Int(required=True)
        title = String()
        body = String()

    post = Field(lambda: PostObject)

    @authorize_user_by_id
    def mutate(root, info, post_id, user_id, title = None, body= None, ):
        session = Session()
        authenticated_user = get_aunthenticated_user(info.context)

        post = session.query(Post).filter(Post.id == post_id,Post.user_id == authenticated_user.id ).first()

        if not post:
            session.close()
            raise Exception("post not found")
        if title is not None:
            post.title = title
        if body is not None:
            post.body = body
        # if user_id is not None:
        #     post.user_id = user_id
        session.commit()
        session.refresh(post)
        session.close()
        return UpdatePost(post=post)

class DeletePost(Mutation):
    class Arguments:
        post_id = Int(required = True)
        user_id = Int(required = True)

    success = Boolean()

    @authorize_user_by_id
    def mutate(root, info, post_id, user_id):
        authenticated_user = get_aunthenticated_user(info.context)
        session = Session()
        post = session.query(Post).filter(Post.id == post_id, Post.user_id == authenticated_user.id).first()

        if not post:
            raise Exception("Post not Found")
        
        session.delete(post)
        session.commit()
        session.close()
        return DeletePost(success = True)
    