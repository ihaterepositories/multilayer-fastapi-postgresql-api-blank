from app.utils.responding.models.base_response import BaseResponse
from app.utils.logging.logger_creator import setup_local_logger

from fastapi import HTTPException
from typing import Any

logger = setup_local_logger("response_logger", "logs/response_logs.log")

def create_ok(message: str, data: Any = None) -> BaseResponse:
    logger.info(f"{message}")
    return BaseResponse(
        status_code=200,
        message=message,
        data_count=calculate_data_count(data),
        data=data
    )

def create_error(message: str, status_code: int = 400) -> BaseResponse:
    logger.error(f"{message}")
    response_body = BaseResponse(
        status_code=status_code,
        message=message,
        data_count=0,
        data=None
    )
    raise HTTPException(status_code=status_code, detail=response_body.model_dump())

def calculate_data_count(data: Any) -> int:
    if data is None:
        return 0
    if isinstance(data, list):
        return len(data)
    return 1