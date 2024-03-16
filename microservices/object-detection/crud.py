from sqlalchemy.orm import Session

import models
import schemas


def get_image(db: Session, image_id: int):
    return db.query(models.Image).filter(models.Image.id == image_id).first()


def get_images(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Image).offset(skip).limit(limit).all()


def create_image(db: Session, image: schemas.ImageCreate):
    db_image = models.Image(image_base_64=image.image_base_64)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def get_boxes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Box).offset(skip).limit(limit).all()


def create_box_image(db: Session, box: schemas.BoxCreate, image_id: int):
    db_box = models.Box(**box.model_dump(), owner_id=image_id)
    db.add(db_box)
    db.commit()
    db.refresh(db_box)
    return db_box
