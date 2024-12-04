from pydantic import BaseModel
from typing import Any, Optional

class BaseResponse(BaseModel):
    status_code: Optional[int]
    message: str
    data_count: Optional[int] = None
    data: Optional[Any] = None