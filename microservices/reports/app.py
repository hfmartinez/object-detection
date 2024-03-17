from microservices.reports import crud, models, schemas
from microservices.reports.database import SessionLocal, engine
from microservices.reports.draw_boxes import DrawBoxes
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import sys

sys.path = ["", ".."] + sys.path[1:]

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["Home"])
def read_root():
    return {"Service": "Reports"}


@app.get("/api/v1/boxes/{image_id}", response_model=schemas.NewImage, tags=["Reports"])
def read_boxes(
    image_id: int,
    label: str = None,
    confidence: float = 0.5,
    db: Session = Depends(get_db),
):
    db_boxes = crud.get_boxes(db, image_id=image_id, label=label, confidence=confidence)
    if not db_boxes:
        raise HTTPException(status_code=404, detail="Data not found")
    db_image = crud.get_image(db, image_id=image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    draw_obj = DrawBoxes()
    new_img_64 = draw_obj.draw_objects(img_64=db_image.image_base_64, boxes=db_boxes)
    new_img = schemas.NewImage(
        image_base_64=db_image.image_base_64,
        id=db_image.id,
        boxes=db_boxes,
        new_image_base_64=new_img_64,
    )
    return new_img
