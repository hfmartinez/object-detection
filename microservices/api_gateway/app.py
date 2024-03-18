from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime, timedelta, timezone
from fastapi.middleware.cors import CORSMiddleware
from microservices.api_gateway.config import global_config
from microservices.api_gateway import schemas
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import requests

app = FastAPI()
api_key_header = global_config.get_api_key()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


urls = global_config.get_urls()
jwt_config = global_config.get_jwt_config()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, jwt_config.get("SECRET_KEY"), algorithm=jwt_config.get("ALGORITHM")
    )
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            jwt_config.get("SECRET_KEY"),
            algorithms=[jwt_config.get("ALGORITHM")],
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/login", tags=["login"])
def login_for_access_token(User: schemas.User):
    if User.username != "test" and User.password != "test":
        raise HTTPException(status_code=404, detail="Error reading images")
    access_token_expires = timedelta(
        minutes=int(jwt_config.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    access_token = create_access_token(
        data={"sub": "test"}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@app.get("/", tags=["Home"])
def read_root():
    return {"Service": "Api-Gateway"}


@app.get("/api/v1/classes/", response_model=list[str], tags=["Images"])
def get_classes(token: str = Depends(oauth2_scheme)):
    decode_token(token=token)
    response = requests.get(
        f"http://{urls.get('OBJECT_DETECTION_URL')}:6000/api/v1/classes/",
        headers={"x-api-key": api_key_header},
    )
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Error reading images")
    return response.json()


@app.post(
    "/api/v1/images/", response_model=schemas.Image, tags=["Object Detection Service"]
)
def create_image(image: schemas.ImageCreate, token: str = Depends(oauth2_scheme)):
    decode_token(token=token)
    data = image.model_dump()
    response = requests.post(
        f"http://{urls.get('OBJECT_DETECTION_URL')}:6000/api/v1/images/",
        json=data,
        headers={"x-api-key": api_key_header},
    )
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Error creating image")
    return response.json()


@app.get(
    "/api/v1/images/",
    response_model=list[schemas.Image],
    tags=["Object Detection Service"],
)
def read_images(skip: int = 0, limit: int = 100, token: str = Depends(oauth2_scheme)):
    decode_token(token=token)
    response = requests.get(
        f"http://{urls.get('OBJECT_DETECTION_URL')}:6000/api/v1/images/",
        params={"skip": skip, "limit": limit},
        headers={"x-api-key": api_key_header},
    )
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Error reading images")
    return response.json()


@app.get(
    "/api/v1/images/{image_id}",
    response_model=schemas.Image,
    tags=["Object Detection Service"],
)
def read_image(image_id: int, token: str = Depends(oauth2_scheme)):
    decode_token(token=token)
    response = requests.get(
        f"http://{urls.get('OBJECT_DETECTION_URL')}:6000/api/v1/images/{image_id}",
        headers={"x-api-key": api_key_header},
    )
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Error reading image")
    return response.json()


@app.delete("/api/v1/images/{image_id}", tags=["Object Detection Service"])
def delete_image(image_id: int, token: str = Depends(oauth2_scheme)):
    decode_token(token=token)
    response = requests.get(
        f"http://{urls.get('OBJECT_DETECTION_URL')}:6000/api/v1/images/{image_id}",
        headers={"x-api-key": api_key_header},
    )
    if response.status_code == 404:
        return HTTPException(status_code=404, detail="Error reading image")
    return response.json()


@app.post(
    "/api/v1/images/{image_id}/boxes/",
    response_model=schemas.Box,
    tags=["Object Detection Service"],
)
def create_box_for_image(
    image_id: int, box: schemas.BoxCreate, token: str = Depends(oauth2_scheme)
):
    decode_token(token=token)
    data = box.model_dump()
    response = requests.post(
        f"http://{urls.get('OBJECT_DETECTION_URL')}:6000/api/v1/images/{image_id}/boxes/",
        json=data,
        headers={"x-api-key": api_key_header},
    )
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Error creating image")
    return response.json()


@app.get(
    "/api/v1/boxes/",
    response_model=list[schemas.Box],
    tags=["Object Detection Service"],
)
def read_items(skip: int = 0, limit: int = 100, token: str = Depends(oauth2_scheme)):
    decode_token(token=token)
    response = requests.get(
        f"http://{urls.get('OBJECT_DETECTION_URL')}:6000/api/v1/boxes/",
        params={"skip": skip, "limit": limit},
        headers={"x-api-key": api_key_header},
    )
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Error reading boxes")
    return response.json()


@app.get("/api/v1/boxes/{image_id}", response_model=schemas.NewImage, tags=["Reports"])
def read_boxes(
    image_id: int,
    label: str = None,
    confidence: float = 0.5,
    token: str = Depends(oauth2_scheme),
):
    decode_token(token=token)
    response = requests.get(
        f"http://{urls.get('REPORTS_URL')}:7000/api/v1/boxes/{image_id}",
        params={"label": label, "confidence": confidence},
        headers={"x-api-key": api_key_header},
    )
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Error reading boxes")
    return response.json()
