from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from microservices.reports.database import Base


class Image(Base):
    __tablename__ = "images"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    image_base_64 = Column(String)

    boxes = relationship("Box", back_populates="owner")
    extend_existing = True


class Box(Base):
    __tablename__ = "boxes"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    x = Column(Integer)
    y = Column(Integer)
    w = Column(Integer)
    h = Column(Integer)
    confidence = Column(Float)
    label = Column(String)
    owner_id = Column(Integer, ForeignKey("images.id"))

    owner = relationship("Image", back_populates="boxes")
