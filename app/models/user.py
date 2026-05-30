from sqlalchemy import Column , String , Boolean , DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

import uuid
from app.core.database import Base

class User(Base):
   
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key = True,
        default=uuid.uuid4
    )

    email = Column(
        String , 
        unique = True,
        nullable =False,
        index = True
    )

    username = Column(
        String,
        unique = True,
        nullable = False,
        index = True
    )

    hashed_password = Column(
        String,
        nullable = False 
    )

    role = Column(
        String,
        default = "user"
    )

    is_verified = Column(
        Boolean,
        default = False
    )

    created_at = Column(
        DateTime(timezone = True),
        server_default = func.now()
    )

    wallet = relationship(
        "Wallet",
        back_populates = "user",
        uselist = False
    )

    #relationship can creates python level navigation between objects.