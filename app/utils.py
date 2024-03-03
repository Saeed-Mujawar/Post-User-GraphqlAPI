from datetime import datetime, timedelta
from datetime import datetime, timezone
from app.settings.config import SECRET_KEY,ALGORITHM,TOKEN_EXPIRATION_TIME_MINUTES
from graphene import Int
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from graphql import GraphQLError
from app.db.database import Session
from app.db.models import User
import jwt
from graphql import GraphQLError
from functools import wraps
# import random
# import string
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

def generate_token(id):
    # now + token lifespan
    expiration_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)
    payload = {
        "sub" : id,
        "exp" : expiration_time
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def hash_password(pwd):
    ph = PasswordHasher()
    return ph.hash(pwd)

def verify_password(pwd_hash, pwd):
    ph = PasswordHasher()
    try:
        ph.verify(pwd_hash, pwd)
    except VerifyMismatchError:
        raise GraphQLError("Invalid password")
    
def get_aunthenticated_user(context):  
    # The context usually contains information about the current request being processed.
    request_object = context.get('request')  
    #  It extracts the Authorization header from the request headers, which typically contains the JWT token.
    
    auth_header = request_object.headers.get('Authorization')   
    token = [None]
    if auth_header:   
    # Splits the Authorization header to extract the token part, which is typically prefixed with "Bearer".
        token = auth_header.split(" ")

    if auth_header and token[0] =="Bearer" and len(token) == 2:
        
       # This is a try-except block that attempts to decode the JWT token. If the token is invalid or expired, it raises appropriate exceptions.
        try:
            #This extracts the payload information from the token.
            payload = jwt.decode(token[1], SECRET_KEY, algorithms=[ALGORITHM])   
            # Checks if the current time is greater than the expiration time (exp) extracted from the token payload
            if datetime.now(timezone.utc) > datetime.fromtimestamp(payload['exp'], tz = timezone.utc):
                raise GraphQLError("Token has expired")
            
            session = Session()
            # Retrieves the user object from the database based on the email address extracted from the token payload.
            user = session.query(User).filter(User.id == payload.get('sub')).first()

            if not user:
                raise GraphQLError("Could not authenticate user")
            return user
        
        except jwt.exceptions.PyJWTError:
            raise GraphQLError("Invalid authentication token")
        except Exception as e:
            raise GraphQLError("Could not authenticate user")
        
        
    else: 
        raise GraphQLError("Missing Authentication token")

def authorize_user_by_id(func):
    @wraps(func) 
    def wrapper(*args, **kwargs):
     
        info = args[1]
        user = get_aunthenticated_user(info.context)
        uid = kwargs.get("user_id")

        if user.id != uid:
            raise GraphQLError("you are not authorized to perform this action")
        
        return func(*args, ** kwargs)
    return wrapper


# def generate_otp(length=6):
#     # Generate a random OTP (one-time password) of specified length.
#     otp = ''.join(random.choices(string.digits, k=length))
#     return otp

# def send_otp_email(email, otp):
    sender_email = "saeedmujawar20@gmail.com"
    receiver_email = email
    password = "xftp oohs yayy dvoo"  # Your app password (generated from Google Account settings)

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "OTP for Email Verification"

    body = f"Your OTP for email verification is: {otp}"
    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")