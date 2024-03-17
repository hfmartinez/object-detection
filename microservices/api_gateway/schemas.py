from pydantic import BaseModel


class BoxBase(BaseModel):
    x: int
    y: int
    w: int
    h: int
    confidence: float
    label: str


class BoxCreate(BoxBase):
    pass


class Box(BoxBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class ImageBase(BaseModel):
    image_base_64: str


class ImageCreate(ImageBase):
    pass


class Image(ImageCreate):
    id: int
    boxes: list[Box] = []

    class Config:
        from_attributes = True


class NewImage(Image):
    new_image_base_64: str
