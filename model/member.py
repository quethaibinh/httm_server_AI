from sqlalchemy import Column, Date, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Member(Base):
    __tablename__ = "member"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(255))
    full_name = Column(String(255))
    phone = Column(String(255))
    avatar_url = Column(String(255))
    gender = Column(String(255))
    date_of_birth = Column(Date)
    address = Column(String(255))
    role = Column(String(255))
    created_at = Column(Date)
    is_active = Column(Boolean, default=True)

    admin = relationship("Admin", back_populates="member", cascade="all, delete-orphan")