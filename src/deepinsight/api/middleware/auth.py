"""认证中间件"""

from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer

# JWT配置
JWT_SECRET = "your-secret-key-change-in-production"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

security = HTTPBearer()


async def auth_middleware(request: Request, call_next):
    """验证请求认证"""
    # 跳过健康检查和公开端点
    if request.url.path in ["/health", "/docs", "/openapi.json"]:
        return await call_next(request)

    # OPTIONS请求（cors预检）直接放行
    if request.method == "OPTIONS":
        return await call_next(request)

    # 检查Authorization头
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
        )

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        request.state.user_id = payload.get("sub")
        request.state.user_role = payload.get("role", "user")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return await call_next(request)


def create_access_token(user_id: str, role: str = "user") -> str:
    """创建JWT访问令牌"""
    expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    payload = {
        "sub": user_id,
        "role": role,
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> dict | None:
    """验证并返回token payload"""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.InvalidTokenError:
        return None
