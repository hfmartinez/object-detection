# from flask import Flask, jsonify, Blueprint, request, abort
# from ObjectDetection import ObjectDetection
# from db import DB
# import uuid

# app = Flask(__name__)

# api_version = Blueprint("api_v1", __name__, url_prefix="/api/v1")


# @api_version.errorhandler(404)
# def resource_not_found(e):
#     return jsonify(error=str(e)), 404


# @api_version.route("/img/detect", methods=["POST"])
# def img():
#     content = request.json
#     print(content)
#     url = content.get("url", "")
#     if not url:
#         abort(404, description="URL")

#     OD = ObjectDetection()
#     img = OD.LoadImgUrl(url)
#     results = OD.detectObj(img)
#     if not results:
#         return jsonify({"msg": "Error getting objects"}), 500
#     img_name = str(uuid.uuid4())
#     response = {"img_name": img_name, "objects": results}

#     db = DB()
#     conn = db.create_connection()
#     for result in results:
#         id = db.save_obj(
#             conn,
#             result.get("box").get("x"),
#             result.get("box").get("y"),
#             result.get("box").get("w"),
#             result.get("box").get("h"),
#             result.get("label"),
#         )
#         db.save_img(conn, img_name, id)
#     db.close_connection(conn)
#     return jsonify(response)


# app.register_blueprint(api_version)


from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Service": "Object-detection"}


@app.post("/api/v1/images/", response_model=schemas.Image)
def create_image(image: schemas.ImageCreate, db: Session = Depends(get_db)):
    # db_user = crud.get_user_by_email(db, email=image.image_base_64)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_image(db=db, image=image)


@app.get("/api/v1/images/", response_model=list[schemas.Image])
def read_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_images(db, skip=skip, limit=limit)
    return users


@app.get("/api/v1/images/{image_id}", response_model=schemas.Image)
def read_image(image_id: int, db: Session = Depends(get_db)):
    db_image = crud.get_image(db, image_id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image


@app.post("/api/v1/images/{image_id}/boxes/", response_model=schemas.Box)
def create_box_for_image(
    image_id: int, box: schemas.BoxCreate, db: Session = Depends(get_db)
):
    return crud.create_box_image(db=db, box=box, image_id=image_id)


@app.get("/api/v1/boxes/", response_model=list[schemas.Box])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    boxes = crud.get_boxes(db, skip=skip, limit=limit)
    return boxes
