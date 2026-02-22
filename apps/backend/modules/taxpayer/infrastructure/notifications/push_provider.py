"""Push Notification Provider implementations"""

from typing import Optional, Dict, Any, List
import aiohttp
import json
from .notification_service import Notification, NotificationProvider


class PushProvider(NotificationProvider):
    """Base push notification provider interface"""
    pass


class FirebasePushProvider(PushProvider):
    """Send push notifications via Firebase Cloud Messaging"""
    
    def __init__(self, project_id: str, credentials_path: str):
        self.project_id = project_id
        self.credentials_path = credentials_path
        self.api_url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"
        self._access_token: Optional[str] = None
    
    async def _get_access_token(self) -> str:
        """Get Firebase access token"""
        try:
            import google.auth
            from google.auth.transport.requests import Request
            
            credentials, _ = google.auth.default(
                scopes=['https://www.googleapis.com/auth/cloud-platform']
            )
            credentials.refresh(Request())
            return credentials.token
        except Exception as e:
            raise RuntimeError(f"Failed to get Firebase token: {str(e)}")
    
    async def send(self, notification: Notification) -> bool:
        """Send push notification via Firebase"""
        try:
            token = await self._get_access_token()
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            }
            
            message = {
                'message': {
                    'token': notification.recipient,
                    'notification': {
                        'title': notification.subject,
                        'body': notification.body,
                    },
                    'data': notification.metadata,
                    'android': {
                        'priority': 'high',
                    },
                    'apns': {
                        'headers': {
                            'apns-priority': '10',
                        },
                    },
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    json=message,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    return response.status == 200
        except Exception as e:
            notification.error = f"Firebase push failed: {str(e)}"
            return False
    
    async def send_batch(self, notifications: List[Notification]) -> Dict[str, bool]:
        """Send multiple push notifications"""
        results = {}
        for notification in notifications:
            results[notification.id] = await self.send(notification)
        return results
    
    async def health_check(self) -> bool:
        """Check Firebase API health"""
        try:
            token = await self._get_access_token()
            # If we can get token, Firebase is healthy
            return bool(token)
        except Exception:
            return False
    
    def get_config(self) -> Dict[str, Any]:
        """Get provider configuration"""
        return {
            'provider': 'firebase',
            'project_id': self.project_id,
        }


class OneSignalPushProvider(PushProvider):
    """Send push notifications via OneSignal"""
    
    def __init__(self, app_id: str, rest_api_key: str):
        self.app_id = app_id
        self.rest_api_key = rest_api_key
        self.api_url = "https://onesignal.com/api/v1/notifications"
    
    async def send(self, notification: Notification) -> bool:
        """Send push notification via OneSignal"""
        try:
            headers = {
                'Authorization': f'Basic {self.rest_api_key}',
                'Content-Type': 'application/json; charset=utf-8',
            }
            
            payload = {
                'app_id': self.app_id,
                'include_external_user_ids': [notification.recipient],
                'headings': {'en': notification.subject},
                'contents': {'en': notification.body},
                'data': notification.metadata,
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    return response.status == 200
        except Exception as e:
            notification.error = f"OneSignal push failed: {str(e)}"
            return False
    
    async def health_check(self) -> bool:
        """Check OneSignal API health"""
        try:
            headers = {
                'Authorization': f'Basic {self.rest_api_key}',
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://onesignal.com/api/v1/apps/{self.app_id}",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    return response.status == 200
        except Exception:
            return False
    
    def get_config(self) -> Dict[str, Any]:
        """Get provider configuration"""
        return {
            'provider': 'onesignal',
            'app_id': self.app_id,
        }


class MockPushProvider(PushProvider):
    """Mock push notification provider for testing"""
    
    def __init__(self):
        self.sent_notifications = []
    
    async def send(self, notification: Notification) -> bool:
        """Mock push send"""
        self.sent_notifications.append({
            'recipient': notification.recipient,
            'subject': notification.subject,
            'body': notification.body,
            'timestamp': notification.created_at,
        })
        return True
    
    async def health_check(self) -> bool:
        """Mock health check"""
        return True
    
    def get_config(self) -> Dict[str, Any]:
        """Get provider configuration"""
        return {'provider': 'mock_push'}
    
    def get_sent_notifications(self) -> List[Dict]:
        """Get all sent notifications for testing"""
        return self.sent_notifications.copy()
