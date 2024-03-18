from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from microservices.object_detection.database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    image_base_64 = Column(String)

    boxes = relationship("Box", back_populates="owner")


class Box(Base):
    __tablename__ = "boxes"

    id = Column(Integer, primary_key=True)
    x = Column(Integer)
    y = Column(Integer)
    w = Column(Integer)
    h = Column(Integer)
    confidence = Column(Float)
    label = Column(String)
    owner_id = Column(Integer, ForeignKey("images.id"))

    owner = relationship("Image", back_populates="boxes")
