
from app.db.models import Image
from app.repository.base import BaseRepository


class ImagesRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(Image, *args, **kwargs)
