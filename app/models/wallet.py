from sqlalchemy import Column , ForeignKey , Numeric , String , Boolean , DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

import uuid
from app.core.database import Base

class Wallet(Base):

    __tablename__ = "wallets"

    id = Column(
        UUID(as_uuid=True),
        primary_key = True,
        default = uuid.uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id"),   #Wallet cannot exist without any users.
        nullable = False
    )

    balance = Column(
        Numeric(12,2),
        default = 0
    )

    currency = Column(
        String,
        default = "INR"
    )

    is_locked = Column(
        Boolean,
        default = False
    )

    created_at = Column(
        DateTime(timezone = True),
        server_default = func.now()
    )