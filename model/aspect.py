from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database import Base

class Aspect(Base):
    __tablename__ = "aspect"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(String(255))

    review_aspects = relationship("ReviewAspect", back_populates="aspect")