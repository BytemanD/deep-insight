"""限流中间件"""

import asyncio
import time
from collections import defaultdict

from fastapi import HTTPException, Request, status

# 简单的内存存储（生产环境应使用Redis）
request_counts: dict[str, list[float]] = defaultdict(list)
_lock = asyncio.Lock()


async def rate_limit_middleware(request: Request, call_next):
    """基于IP的请求限流"""
    # 跳过健康检查
    if request.url.path == "/health":
        return await call_next(request)

    client_ip = request.client.host if request.client else "unknown"
    current_time = time.time()
    window = 60  # 1分钟窗口
    max_requests = 100

    async with _lock:
        # 清理过期记录
        request_counts[client_ip] = [
            t for t in request_counts[client_ip] if current_time - t < window
        ]

        # 检查限流
        if len(request_counts[client_ip]) >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later.",
                headers={"Retry-After": str(window)},
            )

        # 记录请求
        request_counts[client_ip].append(current_time)

    return await call_next(request)
