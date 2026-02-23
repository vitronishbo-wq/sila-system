import pyotp
import qrcode
import io
import base64
from typing import Tuple, Optional
from datetime import datetime, timedelta
import secrets


class MFAProvider:
    """Provedor de autenticação de múltiplos fatores"""
    
    @staticmethod
    def generate_totp_secret() -> str:
        """Gera secret para TOTP"""
        return pyotp.random_base32()
    
    @staticmethod
    def get_totp_uri(secret: str, email: str, issuer: str = "SILA") -> str:
        """Gera URI para configuração do Google Authenticator"""
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(name=email, issuer_name=issuer)
    
    @staticmethod
    def generate_qr_code(uri: str) -> str:
        """Gera QR code em base64 para configuração"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Converte para base64
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_base64}"
    
    @staticmethod
    def verify_totp(secret: str, token: str) -> bool:
        """Verifica token TOTP"""
        totp = pyotp.TOTP(secret)
        return totp.verify(token)
    
    @staticmethod
    def generate_backup_codes(count: int = 8) -> list:
        """Gera códigos de backup para MFA"""
        codes = []
        for _ in range(count):
            # Código de 8 caracteres alfanuméricos
            code = secrets.token_hex(4).upper()
            codes.append(code)
        return codes
    
    @staticmethod
    def verify_backup_code(code: str, stored_codes: list) -> bool:
        """Verifica código de backup"""
        return code.upper() in stored_codes


class EmailMFAProvider:
    """MFA por email"""
    
    def __init__(self):
        self.codes = {}  # user_id -> (code, expires)
    
    def generate_code(self, user_id: str, ttl_minutes: int = 10) -> str:
        """Gera código de verificação"""
        code = ''.join(secrets.choice('0123456789') for _ in range(6))
        expires = datetime.now() + timedelta(minutes=ttl_minutes)
        self.codes[user_id] = (code, expires)
        return code
    
    def verify_code(self, user_id: str, code: str) -> bool:
        """Verifica código"""
        if user_id not in self.codes:
            return False
        
        stored_code, expires = self.codes[user_id]
        if datetime.now() > expires:
            del self.codes[user_id]
            return False
        
        if stored_code == code:
            del self.codes[user_id]
            return True
        
        return False


class SMSMFAProvider(EmailMFAProvider):
    """MFA por SMS (mesma lógica, mas enviaria por SMS)"""
    pass
