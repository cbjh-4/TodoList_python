from pydantic import BaseModel
from datetime import date

class TodoDTO(BaseModel):
    tno: int | None = None
    title: str
    dueDate: date
    finished: bool