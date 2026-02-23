from fastapi import Depends, HTTPException



def get_current_user(token: str = Depends(lambda: 'dev-token')):
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token


def require_permission(permission: str):
    def _dep(user=Depends(get_current_user)):
        if not IAMClient.check_permission(user, permission):
            raise HTTPException(status_code=403, detail="Forbidden")
        return user

    return _dep
