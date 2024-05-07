from pydantic import BaseModel

class MemberDTO(BaseModel):
    mid: str 
    mpw: str
    mname: str | None = None    