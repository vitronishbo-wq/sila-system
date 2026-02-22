"""Email Provider using aiosmtplib"""

from typing import Optional, Dict, Any
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .notification_service import Notification, NotificationProvider


class EmailProvider(NotificationProvider):
    """Send emails via SMTP"""
    
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int = 587,
        use_tls: bool = True,
        username: Optional[str] = None,
        password: Optional[str] = None,
        from_address: str = "noreply@sila.ao",
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.use_tls = use_tls
        self.username = username
        self.password = password
        self.from_address = from_address
    
    async def send(self, notification: Notification) -> bool:
        """Send email notification"""
        try:
            # Create message
            message = MIMEMultipart()
            message['From'] = self.from_address
            message['To'] = notification.recipient
            message['Subject'] = notification.subject
            
            # Add body
            body_part = MIMEText(notification.body, 'html')
            message.attach(body_part)
            
            # Connect and send
            async with aiosmtplib.SMTP(
                hostname=self.smtp_host,
                port=self.smtp_port,
                use_tls=self.use_tls
            ) as client:
                if self.username and self.password:
                    await client.login(self.username, self.password)
                
                await client.send_message(message)
            
            return True
        except Exception as e:
            notification.error = f"Email send failed: {str(e)}"
            return False
    
    async def send_batch(self, notifications: list) -> Dict[str, bool]:
        """Send multiple emails"""
        results = {}
        for notification in notifications:
            results[notification.id] = await self.send(notification)
        return results
    
    async def health_check(self) -> bool:
        """Check SMTP connection health"""
        try:
            async with aiosmtplib.SMTP(
                hostname=self.smtp_host,
                port=self.smtp_port,
                use_tls=self.use_tls,
                timeout=10
            ) as client:
                # EHLO command to check server
                await client.ehlo()
            return True
        except Exception:
            return False
    
    def get_config(self) -> Dict[str, Any]:
        """Get provider configuration"""
        return {
            'provider': 'smtp',
            'host': self.smtp_host,
            'port': self.smtp_port,
            'use_tls': self.use_tls,
            'from_address': self.from_address,
            'authenticated': bool(self.username),
        }


class SendgridEmailProvider(NotificationProvider):
    """Alternative: Send emails via Sendgrid API"""
    
    def __init__(self, api_key: str, from_address: str = "noreply@sila.ao"):
        self.api_key = api_key
        self.from_address = from_address
    
    async def send(self, notification: Notification) -> bool:
        """Send email via Sendgrid"""
        import aiohttp
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
            }
            
            payload = {
                'personalizations': [{
                    'to': [{'email': notification.recipient}]
                }],
                'from': {'email': self.from_address},
                'subject': notification.subject,
                'content': [{
                    'type': 'text/html',
                    'value': notification.body
                }],
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://api.sendgrid.com/v3/mail/send',
                    json=payload,
                    headers=headers,
                ) as response:
                    return response.status == 202
        except Exception as e:
            notification.error = f"Sendgrid send failed: {str(e)}"
            return False
    
    async def health_check(self) -> bool:
        """Check Sendgrid API health"""
        import aiohttp
        
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    'https://api.sendgrid.com/v3/mail/send',
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    return response.status in [200, 405]  # 405 because we're just checking endpoint
        except Exception:
            return False
    
    def get_config(self) -> Dict[str, Any]:
        """Get provider configuration"""
        return {
            'provider': 'sendgrid',
            'from_address': self.from_address,
        }
