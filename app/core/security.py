from datetime import datetime, timedelta,timezone
from jose import JWTError, jwt  
from passlib.context import CryptContext
from app.core.config import settings

# Use passlib's built-in PBKDF2 backend to avoid bcrypt backend issues on some runtimes.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)
   

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict)->str:
    to_encode = data.copy() #original data ko change nhi krna chahte isliye copy kr rhe hai
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm    
    )
