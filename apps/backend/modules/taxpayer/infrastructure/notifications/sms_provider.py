"""SMS Provider implementations"""

from typing import Optional, Dict, Any
import aiohttp
from .notification_service import Notification, NotificationProvider


class SMSProvider(NotificationProvider):
    """Base SMS provider interface"""
    pass


class TwilioSMSProvider(SMSProvider):
    """Send SMS via Twilio API"""
    
    def __init__(
        self,
        account_sid: str,
        auth_token: str,
        from_number: str,
    ):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number
        self.api_url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
    
    async def send(self, notification: Notification) -> bool:
        """Send SMS via Twilio"""
        try:
            auth = aiohttp.BasicAuth(self.account_sid, self.auth_token)
            
            data = {
                'From': self.from_number,
                'To': notification.recipient,
                'Body': notification.body[:160],  # SMS character limit
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    data=data,
                    auth=auth,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    result = await response.json()
                    return response.status == 201 and 'sid' in result
        except Exception as e:
            notification.error = f"Twilio SMS failed: {str(e)}"
            return False
    
    async def health_check(self) -> bool:
        """Check Twilio API health"""
        try:
            auth = aiohttp.BasicAuth(self.account_sid, self.auth_token)
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}.json",
                    auth=auth,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    return response.status == 200
        except Exception:
            return False
    
    def get_config(self) -> Dict[str, Any]:
        """Get provider configuration"""
        return {
            'provider': 'twilio',
            'from_number': self.from_number,
        }


class AfricasTalkingSMSProvider(SMSProvider):
    """Send SMS via Africas Talking API (Angola-based)"""
    
    def __init__(
        self,
        api_key: str,
        username: str = "sandbox",
        sender_id: str = "SILASystem",
    ):
        self.api_key = api_key
        self.username = username
        self.sender_id = sender_id
        self.api_url = "https://api.sandbox.africastalking.com/version1/messaging"
    
    async def send(self, notification: Notification) -> bool:
        """Send SMS via Africas Talking"""
        try:
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
                'ApiKey': self.api_key,
            }
            
            # Ensure phone number has country code
            phone = notification.recipient
            if not phone.startswith('+'):
                if phone.startswith('244'):
                    phone = f'+{phone}'
                else:
                    phone = f'+244{phone}'
            
            data = {
                'username': self.username,
                'to': phone,
                'message': notification.body[:160],
                'from': self.sender_id,
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    data=data,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        # Check if message was queued successfully
                        return result.get('SMSMessageData', {}).get('Recipients', [{}])[0].get('statusCode') == '101'
                    return False
        except Exception as e:
            notification.error = f"Africas Talking SMS failed: {str(e)}"
            return False
    
    async def health_check(self) -> bool:
        """Check Africas Talking API health"""
        try:
            headers = {
                'Accept': 'application/json',
                'ApiKey': self.api_key,
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://api.sandbox.africastalking.com/version1/user",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    return response.status == 200
        except Exception:
            return False
    
    def get_config(self) -> Dict[str, Any]:
        """Get provider configuration"""
        return {
            'provider': 'africas_talking',
            'username': self.username,
            'sender_id': self.sender_id,
        }


class MockSMSProvider(SMSProvider):
    """Mock SMS provider for testing"""
    
    def __init__(self):
        self.sent_messages = []
    
    async def send(self, notification: Notification) -> bool:
        """Mock SMS send"""
        self.sent_messages.append({
            'recipient': notification.recipient,
            'body': notification.body,
            'timestamp': notification.created_at,
        })
        return True
    
    async def health_check(self) -> bool:
        """Mock health check"""
        return True
    
    def get_config(self) -> Dict[str, Any]:
        """Get provider configuration"""
        return {'provider': 'mock_sms'}
