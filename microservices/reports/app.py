from microservices.reports import crud, models, schemas
from microservices.reports.database import SessionLocal, engine
from microservices.reports.draw_boxes import DrawBoxes
from microservices.reports.config import global_config
from microservices.reports.utils import redis_manager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
import sys

sys.path = ["", ".."] + sys.path[1:]

models.Base.metadata.create_all(bind=engine)
api_key_header = APIKeyHeader(name="x-api-key")
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate_api_key(api_key: str):
    if api_key != global_config.get_api_key():
        raise HTTPException(401, "Invalid credentials")
    return True


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
    api_key: str = Security(api_key_header),
    db: Session = Depends(get_db),
):
    validate_api_key(api_key)
    response = redis_manager(key=f"{image_id}", operation="read")
    response_boxes = redis_manager(key=f"{image_id}_boxes", operation="read")
    if not response or not response_boxes:
        db_boxes = crud.get_boxes(
            db, image_id=image_id, label=label, confidence=confidence
        )
        if not db_boxes:
            raise HTTPException(status_code=404, detail="Data not found")
        db_image = crud.get_image(db, image_id=image_id)
        if not db_image:
            raise HTTPException(status_code=404, detail="Image not found")
        draw_obj = DrawBoxes()
        new_img_64 = draw_obj.draw_objects(
            img_64=db_image.image_base_64, boxes=db_boxes
        )
        new_img = schemas.NewImage(
            image_base_64=db_image.image_base_64,
            id=db_image.id,
            boxes=db_boxes,
            new_image_base_64=new_img_64,
        )
        return new_img
    draw_obj = DrawBoxes()
    new_img_64 = draw_obj.draw_objects(
        img_64=response["image_base_64"], boxes=response_boxes, confidence=confidence
    )
    new_img = schemas.NewImage(
        image_base_64=response["image_base_64"],
        id=response["id"],
        boxes=response_boxes,
        new_image_base_64=new_img_64,
    )
    return new_img
