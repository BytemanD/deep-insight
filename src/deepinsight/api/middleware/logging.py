"""日志中间件"""

import time

from fastapi import Request
from loguru import logger


async def logging_middleware(request: Request, call_next):
    """请求日志记录"""
    start_time = time.time()

    # 请求日志
    logger.info(
        f"Request started: {request.method} {request.url.path}",
        extra={
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host if request.client else None,
        },
    )

    response = await call_next(request)

    # 响应日志
    duration = time.time() - start_time
    logger.info(
        f"Request completed: {request.method} {request.url.path} - {response.status_code} ({duration:.3f}s)",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration": duration,
        },
    )

    return response
