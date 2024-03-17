from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from microservices.api_gateway.config import global_config
from microservices.api_gateway import schemas
import requests

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

urls = global_config.get_urls()


@app.get("/", tags=["Home"])
def read_root():
    return {"Service": "Api-Gateway"}


@app.get("/api/v1/classes/", response_model=list[str], tags=["Images"])
def get_classes():
    response = requests.get(
        f"http://{urls.get('OBJECT_DETECTION_URL')}:6000/api/v1/classes/"
    )
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Error reading images")
    return response.json()


@app.post(
    "/api/v1/images/", response_model=schemas.Image, tags=["Object Detection Service"]
)
def create_image(image: schemas.ImageCreate):
    data = image.model_dump()
    response = requests.post(
        f"http://{urls.get('OBJECT_DETECTION_URL')}:6000/api/v1/images/", json=data
    )
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Error creating image")
    return response.json()


@app.get(
    "/api/v1/images/",
    response_model=list[schemas.Image],
    tags=["Object Detection Service"],
)
def read_images(skip: int = 0, limit: int = 100):
    response = requests.get(
        f"http://{urls.get('OBJECT_DETECTION_URL')}:6000/api/v1/images/",
        params={"skip": skip, "limit": limit},
    )
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Error reading images")
    return response.json()


@app.get(
    "/api/v1/images/{image_id}",
    response_model=schemas.Image,
    tags=["Object Detection Service"],
)
def read_image(image_id: int):
    response = requests.get(
        f"http://{urls.get('OBJECT_DETECTION_URL')}:6000/api/v1/images/{image_id}"
    )
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Error reading image")
    return response.json()


@app.delete("/api/v1/images/{image_id}", tags=["Object Detection Service"])
def delete_image(image_id: int):
    response = requests.get(
        f"http://{urls.get('OBJECT_DETECTION_URL')}:6000/api/v1/images/{image_id}"
    )
    if response.status_code == 404:
        return HTTPException(status_code=404, detail="Error reading image")
    return response.json()


@app.post(
    "/api/v1/images/{image_id}/boxes/",
    response_model=schemas.Box,
    tags=["Object Detection Service"],
)
def create_box_for_image(image_id: int, box: schemas.BoxCreate):
    data = box.model_dump()
    response = requests.post(
        f"http://{urls.get('OBJECT_DETECTION_URL')}:6000/api/v1/images/{image_id}/boxes/",
        json=data,
    )
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Error creating image")
    return response.json()


@app.get(
    "/api/v1/boxes/",
    response_model=list[schemas.Box],
    tags=["Object Detection Service"],
)
def read_items(skip: int = 0, limit: int = 100):
    response = requests.get(
        f"http://{urls.get('OBJECT_DETECTION_URL')}:6000/api/v1/boxes/",
        params={"skip": skip, "limit": limit},
    )
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Error reading boxes")
    return response.json()


@app.get("/api/v1/boxes/{image_id}", response_model=schemas.NewImage, tags=["Reports"])
def read_boxes(image_id: int, label: str = None, confidence: float = 0.5):
    response = requests.get(
        f"http://{urls.get('REPORTS_URL')}:7000/api/v1/boxes/{image_id}",
        params={"label": label, "confidence": confidence},
    )
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Error reading boxes")
    return response.json()
