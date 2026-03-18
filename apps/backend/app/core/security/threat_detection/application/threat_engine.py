import time
import hashlib

class ThreatEngine:
    """Threat detection and IP reputation engine"""
    blacklist = set()
    suspicious_ips = {}

    def register_ip(self, ip):
        """Register IP and track suspicious patterns"""
        if ip in self.blacklist:
            return 'blocked'
        now = time.time()
        if ip not in self.suspicious_ips:
            self.suspicious_ips[ip] = []
        self.suspicious_ips[ip].append(now)
        self.suspicious_ips[ip] = [t for t in self.suspicious_ips[ip] if now - t < 60]
        if len(self.suspicious_ips[ip]) > 200:
            self.blacklist.add(ip)
            return 'blacklisted'
        return 'ok'