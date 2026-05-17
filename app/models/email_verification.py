import uuid
from sqlalchemy import Column, String, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.user import GUID


class EmailVerification(Base):
    __tablename__ = "email_verifications"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False)
    code = Column(String(6), nullable=False)
    type = Column(String(20), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())


class CookieConsent(Base):
    __tablename__ = "cookie_consents"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    session_id = Column(String(100))
    necessary = Column(Boolean, default=True)
    analytics = Column(Boolean, default=False)
    marketing = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="cookie_consents")
