from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Admin():
    __tablename__ = "admin"

    member_id = Column(Integer, ForeignKey("member.id"), primary_key=True)
    
    member = relationship("Member", back_populates="admin")