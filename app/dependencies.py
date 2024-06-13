from uuid import uuid4

from fastapi import HTTPException

def generate_uuid():
    return str(uuid4())

def check_active(user):
    if not user.is_active:
        raise HTTPException(status_code=401,
                             detail=f"Недостаточно прав. Пользователь деактивирован")
def check_rights(user, roles, error_msg):
    if user.role_name not in roles:
        raise HTTPException(status_code=401,
                             detail=f"Недостаточно прав. {error_msg}")
    check_active(user)