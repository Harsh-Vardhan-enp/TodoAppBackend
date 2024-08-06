import bcrypt
import jwt
from sqlalchemy import Boolean, Column, DateTime, Integer, LargeBinary, PrimaryKeyConstraint, String, UniqueConstraint
from src.db import Base
import src.settings

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, nullable=False, primary_key= True)
    email = Column(String(100), nullable=True, unique=True )
    name = Column(String(100), nullable=True, unique=False )
    hashed_pass = Column(LargeBinary, nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime)

    UniqueConstraint("email", name="unique_user_email")
    PrimaryKeyConstraint("id", name="pk_user_id")

    @staticmethod
    def hash_password(pwd) -> str:
        return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
    
    def validate_password(self, pwd) -> bool:
        return bcrypt.checkpw(pwd.encode(), self.hashed_pass)
    
    def gen_token(self) -> dict:
        return {
            "access_token": jwt.encode(
                {
                    "name": self.name,
                    "id":self.id
                },
                src.settings.SECRET_KEY
            )
        }