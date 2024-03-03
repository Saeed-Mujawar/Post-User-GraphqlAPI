from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings.config import DB_URL
# from app.db.models import Base, Post, User
# from app.db.data import post_data, user_data


engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine)

# def prepare_database():
#     # from app.utils import hash_password

#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)

#     session =  Session()

#     for user in user_data:
#         users = User(**user)
#         session.add(users)

#     for post in post_data:
#         session.add(Post(**post))

#     # for user in user_data:
#     #     user['password_hash'] = hash_password(user['password'])
#     #     del user['password']
#     #     session.add(User(**user))

#     session.commit()
#     session.close()