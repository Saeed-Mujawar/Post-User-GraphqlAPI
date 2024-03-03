from graphene import Mutation, String, Int, Field, Boolean
from graphql import GraphQLError
from app.gql.schemas import UserObject
from app.db.database import Session
from app.db.models import User, Post
from app.utils import generate_token, verify_password, hash_password, authorize_user_by_id

class LoginUser(Mutation):

    class Arguments:
        email = String(required = True)
        password = String(required = True)
    token = String()

    @staticmethod
    def mutate(root, info, email, password):
        session = Session()
        user = session.query(User).filter(User.email == email).first()
        if not user:
            raise GraphQLError("A user by that email does not exist ")
        
        verify_password(user.password_hash, password)        
        
        token = generate_token(user.id)

        return LoginUser(token = token)

class AddUser(Mutation):
    class Arguments:
        username = String(required = True)
        email = String(required = True)
        password = String(required = True)
    user = Field(lambda: UserObject)

    @staticmethod
    def mutate(root, info, username, email,password):

        session = Session()
        existing_user  = session.query(User).filter(User.email == email).first()

        if existing_user :
            raise GraphQLError("A user wuth thet email already exists")
        

        password_hash = hash_password(password)
        user = User(username = username, email = email, password_hash = password_hash)

        session.add(user)
        session.commit()
        session.refresh(user)


        # otp = generate_otp()
        # send_otp_email(email, otp)

        return AddUser(user = user)
    

class DeleteUser(Mutation):
    class Arguments:
        user_id = Int(required = True)

    success = Boolean()

    @staticmethod
    @authorize_user_by_id
    def mutate(root, info, user_id):
        session = Session()
        user = session.query(User).filter(User.id == user_id).first()

        if not user:
            raise Exception("User not Found")
        
        user_posts = session.query(Post).filter(Post.user_id == user_id).all()
        for post in user_posts:
            session.delete(post)
        
        session.delete(user)
        session.commit()
        session.close()
        return DeleteUser(success = True)
    
class UpdateUser(Mutation):
    class Arguments:
        user_id = Int(required = True)
        username = String()
        email = String()
        password = String()

    user = Field(lambda: UserObject)

    @staticmethod
    @authorize_user_by_id
    def mutate(root, info, user_id, username = None, email= None, password= None):
        
        session = Session()
        user = session.query(User).filter(User.id == user_id).first()

        if not user:
            raise GraphQLError("user not found")
        if username is not None:
            user.username = username
        if email is not None:
            user.email = email
        if password is not None:
            if not password:
                raise GraphQLError("Password cannot be empty")
            password_hash = hash_password(password)
            user.password_hash = password_hash
        session.commit()
        session.refresh(user)
        session.close()
        return UpdateUser(user=user)
    
# class VerifyOTP(Mutation):
#     class Arguments:
#         email = String(required=True)
#         otp = String(required=True)

#     success = Boolean()

#     @staticmethod
#     def mutate(root, info, email, otp):
#         session = Session() 

#         user = session.query(User).filter(User.email == email).first()
#         if not user:
#             session.close()
#             raise GraphQLError("User not found")

#         # Verify OTP
#         if user.otp != otp:
#             session.close()
#             raise GraphQLError("Invalid OTP")

#         # Mark the user's email as verified
#         user.email_verified = True
#         user.otp = None  # Clear the OTP after verification
#         session.commit()

#         # Close the session
#         session.close()

#         return VerifyOTP(success=True)