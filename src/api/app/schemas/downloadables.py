from pydantic import BaseModel
from pydantic.types import Json,Dict

class Downloadable(BaseModel):
    layerId:int
    fileName:str