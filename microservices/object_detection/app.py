import crud
import models
import schemas
from database import SessionLocal, engine
from object_detection import ObjectDetection
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["Home"])
def read_root():
    return {"Service": "Object-detection"}


@app.post("/api/v1/images/", response_model=schemas.Image, tags=["Images"])
def create_image(image: schemas.ImageCreate, db: Session = Depends(get_db)):
    db_img = crud.get_img_by_64(db, image_base_64=image.image_base_64)
    if not db_img:
        obj_detection_model = ObjectDetection()
        img = obj_detection_model.load_img_base_64(img_64=image.image_base_64)
        boxes = obj_detection_model.detect_obj(img)
        if not boxes:
            return HTTPException(status_code=404, detail="Image not found")
        db_img = crud.create_image(db=db, image=image)
        if not db_img:
            return HTTPException(status_code=404, detail="Error creating image")
        for box in boxes:
            crud.create_box_image(db=db, box=box, image_id=db_img.id)

    return crud.get_img_by_64(db, image_base_64=image.image_base_64)


@app.get("/api/v1/images/", response_model=list[schemas.Image], tags=["Images"])
def read_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_images(db, skip=skip, limit=limit)
    return users


@app.get("/api/v1/images/{image_id}", response_model=schemas.Image, tags=["Images"])
def read_image(image_id: int, db: Session = Depends(get_db)):
    db_image = crud.get_image(db, image_id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image


@app.delete("/api/v1/images/{image_id}", tags=["Images"])
def delete_image(image_id: int, db=Depends(get_db)):
    return crud.delete_img(db, image_id=image_id)


@app.post("/api/v1/images/{image_id}/boxes/", response_model=schemas.Box, tags=["Box"])
def create_box_for_image(
    image_id: int, box: schemas.BoxCreate, db: Session = Depends(get_db)
):
    return crud.create_box_image(db=db, box=box, image_id=image_id)


@app.get("/api/v1/boxes/", response_model=list[schemas.Box], tags=["Box"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    boxes = crud.get_boxes(db, skip=skip, limit=limit)
    return boxes
