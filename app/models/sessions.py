from uuid import uuid4
from sqlalchemy import Boolean , DateTime , ForeignKey , String , Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import sqlalchemy as sa

from app.core.database import Base

class Session(Base):

    __tablename__ = "sessions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    refresh_jti = Column(String(255), nullable=False, unique=True)

    device_name = Column(String(255), nullable=True)

    ip_address = Column(String(45), nullable=True)

    user_agent = Column(String(500), nullable=True)

    revoked = Column(Boolean, default=False, nullable=False)

    expires_at = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="sessions")

    reuse_detected = Column(Boolean,default=False,nullable=False,server_default=sa.false())