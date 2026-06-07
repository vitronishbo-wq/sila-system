import base64
from io import BytesIO

import pyotp
import qrcode
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr


class SetupRequest(BaseModel):
    email: EmailStr


class SetupResponse(BaseModel):
    secret: str
    provisioning_uri: str
    qr_code_b64: str


class VerifyRequest(BaseModel):
    secret: str
    token: str


app = FastAPI()


@app.post("/mfa/setup", response_model=SetupResponse)
async def mfa_setup(req: SetupRequest):
    # Gera secret (salvar no DB criptografado)
    secret = pyotp.random_base32()
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=req.email, issuer_name="SilaSystem")

    qr = qrcode.make(uri)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()

    return SetupResponse(secret=secret, provisioning_uri=uri, qr_code_b64=b64)


@app.post("/mfa/verify-setup")
async def verify_setup(req: VerifyRequest):
    totp = pyotp.TOTP(req.secret)
    if totp.verify(req.token, valid_window=1):
        return {"verified": True}
    raise HTTPException(status_code=400, detail="Invalid token")


@app.post("/mfa/verify-login")
async def verify_login(req: VerifyRequest):
    # Reutiliza lógica de verificação (no mundo real, recupere secret do DB)
    return await verify_setup(req)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("scripts.mfa_example_fastapi:app", host="127.0.0.1", port=8000, reload=True)
