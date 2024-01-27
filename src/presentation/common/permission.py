from functools import wraps
from fastapi import HTTPException


def check_role(allowed_roles: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get("user")
            if user.get("role") not in allowed_roles:
                raise HTTPException(
                    status_code=403,
                    detail={"message": "permission danied", "code": "403"},
                )
            return await func(*args, **kwargs)

        return wrapper

    return decorator
