"""Immutable logging service for secure audit trails."""

import base64
import hashlib
import hmac
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from cryptography.fernet import Fernet
from sqlalchemy.orm import Session

from ..models.audit_log import AuditLog


class ImmutableLogger:
    """Service for creating immutable, tamper-proof audit logs."""

    def __init__(self, db: Session, encryption_key: Optional[bytes] = None):
        self.db = db
        self.encryption_key = encryption_key or self._get_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.hmac_key = self._derive_hmac_key()

    def create_immutable_log(
        self, audit_log: AuditLog, previous_hash: Optional[str] = None
    ) -> str:
        """Create an immutable audit log entry with cryptographic hash chain."""
        # Get the previous log's hash if not provided
        if previous_hash is None:
            previous_hash = self._get_last_log_hash()

        # Create log data structure
        log_data = self._prepare_log_data(audit_log)

        # Generate hash chain
        current_hash = self._generate_hash_chain(log_data, previous_hash)

        # Create digital signature
        signature = self._create_digital_signature(log_data, current_hash)

        # Encrypt sensitive data
        encrypted_data = self._encrypt_sensitive_data(log_data)

        # Store immutable record
        audit_log.hash_value = current_hash
        audit_log.additional_data = audit_log.additional_data or {}
        audit_log.additional_data.update(
            {
                "immutable_signature": signature,
                "encrypted_fields": encrypted_data,
                "chain_verified": True,
                "previous_hash": previous_hash,
            }
        )

        return current_hash

    def verify_log_integrity(self, audit_log: AuditLog) -> Dict[str, Any]:
        """Verify the integrity of an immutable audit log."""
        verification_result = {
            "log_id": audit_log.id,
            "is_valid": False,
            "hash_valid": False,
            "signature_valid": False,
            "chain_valid": False,
            "encryption_valid": False,
            "errors": [],
        }

        try:
            # Verify hash
            log_data = self._prepare_log_data(audit_log)
            previous_hash = audit_log.additional_data.get("previous_hash", "")
            expected_hash = self._generate_hash_chain(log_data, previous_hash)

            verification_result["hash_valid"] = expected_hash == audit_log.hash_value
            if not verification_result["hash_valid"]:
                verification_result["errors"].append("Hash verification failed")

            # Verify digital signature
            stored_signature = audit_log.additional_data.get("immutable_signature")
            if stored_signature:
                signature_valid = self._verify_digital_signature(
                    log_data, audit_log.hash_value, stored_signature
                )
                verification_result["signature_valid"] = signature_valid
                if not signature_valid:
                    verification_result["errors"].append(
                        "Digital signature verification failed"
                    )
            else:
                verification_result["errors"].append("No digital signature found")

            # Verify chain integrity
            chain_valid = self._verify_chain_integrity(audit_log)
            verification_result["chain_valid"] = chain_valid
            if not chain_valid:
                verification_result["errors"].append("Hash chain verification failed")

            # Verify encryption
            encrypted_data = audit_log.additional_data.get("encrypted_fields")
            if encrypted_data:
                try:
                    self._decrypt_sensitive_data(encrypted_data)
                    verification_result["encryption_valid"] = True
                except Exception:
                    verification_result["encryption_valid"] = False
                    verification_result["errors"].append(
                        "Encryption verification failed"
                    )
            else:
                verification_result["encryption_valid"] = True  # No encryption required

            # Overall validity
            verification_result["is_valid"] = (
                verification_result["hash_valid"]
                and verification_result["signature_valid"]
                and verification_result["chain_valid"]
                and verification_result["encryption_valid"]
            )

        except Exception as e:
            verification_result["errors"].append(f"Verification error: {str(e)}")

        return verification_result

    def verify_log_chain(
        self, start_id: Optional[int] = None, end_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Verify the integrity of the entire audit log chain."""
        query = self.db.query(AuditLog).order_by(AuditLog.id)

        if start_id:
            query = query.filter(AuditLog.id >= start_id)
        if end_id:
            query = query.filter(AuditLog.id <= end_id)

        logs = query.all()

        chain_result = {
            "total_logs": len(logs),
            "valid_logs": 0,
            "invalid_logs": 0,
            "chain_breaks": [],
            "is_chain_valid": True,
            "verification_details": [],
        }

        previous_hash = None

        for i, log in enumerate(logs):
            # Verify individual log
            log_verification = self.verify_log_integrity(log)

            if log_verification["is_valid"]:
                chain_result["valid_logs"] += 1
            else:
                chain_result["invalid_logs"] += 1
                chain_result["is_chain_valid"] = False

            # Check chain continuity
            expected_previous_hash = (
                log.additional_data.get("previous_hash")
                if log.additional_data
                else None
            )

            if i > 0 and expected_previous_hash != previous_hash:
                chain_result["chain_breaks"].append(
                    {
                        "log_id": log.id,
                        "expected_previous_hash": expected_previous_hash,
                        "actual_previous_hash": previous_hash,
                    }
                )
                chain_result["is_chain_valid"] = False

            chain_result["verification_details"].append(
                {
                    "log_id": log.id,
                    "is_valid": log_verification["is_valid"],
                    "errors": log_verification["errors"],
                }
            )

            previous_hash = log.hash_value

        return chain_result

    def create_audit_snapshot(self) -> Dict[str, Any]:
        """Create a cryptographic snapshot of the audit log state."""
        # Get all audit logs
        all_logs = self.db.query(AuditLog).order_by(AuditLog.id).all()

        # Create merkle tree of all log hashes
        log_hashes = [log.hash_value for log in all_logs]
        merkle_root = self._calculate_merkle_root(log_hashes)

        # Create snapshot metadata
        snapshot = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_logs": len(all_logs),
            "merkle_root": merkle_root,
            "first_log_id": all_logs[0].id if all_logs else None,
            "last_log_id": all_logs[-1].id if all_logs else None,
            "snapshot_hash": None,
        }

        # Generate snapshot hash
        snapshot_data = json.dumps(snapshot, sort_keys=True, default=str)
        snapshot["snapshot_hash"] = hashlib.sha256(snapshot_data.encode()).hexdigest()

        return snapshot

    def detect_tampering(self) -> List[Dict[str, Any]]:
        """Detect potential tampering in audit logs."""
        tampering_indicators = []

        # Check for hash chain breaks
        chain_verification = self.verify_log_chain()
        if not chain_verification["is_chain_valid"]:
            tampering_indicators.append(
                {
                    "type": "chain_break",
                    "severity": "critical",
                    "description": "Hash chain integrity compromised",
                    "details": chain_verification["chain_breaks"],
                }
            )

        # Check for timestamp anomalies
        timestamp_anomalies = self._detect_timestamp_anomalies()
        if timestamp_anomalies:
            tampering_indicators.append(
                {
                    "type": "timestamp_anomaly",
                    "severity": "medium",
                    "description": "Suspicious timestamp patterns detected",
                    "details": timestamp_anomalies,
                }
            )

        # Check for duplicate hashes
        duplicate_hashes = self._detect_duplicate_hashes()
        if duplicate_hashes:
            tampering_indicators.append(
                {
                    "type": "duplicate_hash",
                    "severity": "high",
                    "description": "Duplicate hash values detected",
                    "details": duplicate_hashes,
                }
            )

        # Check for missing logs
        missing_logs = self._detect_missing_logs()
        if missing_logs:
            tampering_indicators.append(
                {
                    "type": "missing_logs",
                    "severity": "high",
                    "description": "Gaps in log sequence detected",
                    "details": missing_logs,
                }
            )

        return tampering_indicators

    # ============================================================================
    # PRIVATE HELPER METHODS
    # ============================================================================

    def _get_encryption_key(self) -> bytes:
        """Get or generate encryption key."""
        # In production, this should come from secure key management
        key_env = settings.MONITORING_ENCRYPTION_KEY
        if key_env:
            return base64.urlsafe_b64decode(key_env.encode())

        # Generate new key (should be stored securely)
        # Derive HMAC key from encryption key
        return hashlib.sha256(self.encryption_key + b"hmac").digest()

    def _prepare_log_data(self, audit_log: AuditLog) -> Dict[str, Any]:
        """Prepare audit log data for hashing."""
        return {
            "id": audit_log.id,
            "user_id": audit_log.user_id,
            "user_email": audit_log.user_email,
            "action": audit_log.action.value if audit_log.action else None,
            "level": audit_log.level.value if audit_log.level else None,
            "module": audit_log.module,
            "resource_type": audit_log.resource_type,
            "resource_id": audit_log.resource_id,
            "description": audit_log.description,
            "timestamp": (
                audit_log.timestamp.isoformat() if audit_log.timestamp else None
            ),
            "success": audit_log.success,
            "ip_address": audit_log.ip_address,
            "session_id": audit_log.session_id,
        }

    def _get_last_log_hash(self) -> str:
        """Get the hash of the last audit log."""
        last_log = self.db.query(AuditLog).order_by(AuditLog.id.desc()).first()

        return last_log.hash_value if last_log else "genesis"

    def _generate_hash_chain(self, log_data: Dict[str, Any], previous_hash: str) -> str:
        """Generate hash for the log chain."""
        # Create deterministic string from log data
        log_string = json.dumps(log_data, sort_keys=True, default=str)

        # Combine with previous hash
        chain_data = f"{previous_hash}:{log_string}"

        # Generate SHA-256 hash
        return hashlib.sha256(chain_data.encode()).hexdigest()

    def _create_digital_signature(
        self, log_data: Dict[str, Any], current_hash: str
    ) -> str:
        """Create HMAC-based digital signature."""
        signature_data = (
            f"{json.dumps(log_data, sort_keys=True, default=str)}:{current_hash}"
        )

        return hmac.new(
            self.hmac_key, signature_data.encode(), hashlib.sha256
        ).hexdigest()

    def _verify_digital_signature(
        self, log_data: Dict[str, Any], current_hash: str, stored_signature: str
    ) -> bool:
        """Verify HMAC-based digital signature."""
        expected_signature = self._create_digital_signature(log_data, current_hash)
        return hmac.compare_digest(expected_signature, stored_signature)

    def _encrypt_sensitive_data(self, log_data: Dict[str, Any]) -> Dict[str, str]:
        """Encrypt sensitive fields in log data."""
        sensitive_fields = ["user_email", "ip_address", "session_id", "description"]
        encrypted_data = {}

        for field in sensitive_fields:
            if field in log_data and log_data[field]:
                encrypted_value = self.cipher_suite.encrypt(
                    str(log_data[field]).encode()
                )
                encrypted_data[field] = base64.b64encode(encrypted_value).decode()

        return encrypted_data

    def _decrypt_sensitive_data(self, encrypted_data: Dict[str, str]) -> Dict[str, str]:
        """Decrypt sensitive fields."""
        decrypted_data = {}

        for field, encrypted_value in encrypted_data.items():
            try:
                encrypted_bytes = base64.b64decode(encrypted_value.encode())
                decrypted_bytes = self.cipher_suite.decrypt(encrypted_bytes)
                decrypted_data[field] = decrypted_bytes.decode()
            except Exception:
                raise ValueError(f"Failed to decrypt field: {field}")

        return decrypted_data

    def _verify_chain_integrity(self, audit_log: AuditLog) -> bool:
        """Verify the chain integrity for a specific log."""
        if not audit_log.additional_data:
            return False

        previous_hash = audit_log.additional_data.get("previous_hash")
        if not previous_hash:
            return False

        # Find the previous log
        previous_log = (
            self.db.query(AuditLog)
            .filter(AuditLog.id < audit_log.id)
            .order_by(AuditLog.id.desc())
            .first()
        )

        if not previous_log and previous_hash != "genesis":
            return False

        if previous_log and previous_log.hash_value != previous_hash:
            return False

        return True

    def _calculate_merkle_root(self, hashes: List[str]) -> str:
        """Calculate Merkle root of hash list."""
        if not hashes:
            return hashlib.sha256(b"empty").hexdigest()

        if len(hashes) == 1:
            return hashes[0]

        # Pad with duplicate if odd number
        if len(hashes) % 2 == 1:
            hashes.append(hashes[-1])

        # Calculate next level
        next_level = []
        for i in range(0, len(hashes), 2):
            combined = f"{hashes[i]}:{hashes[i+1]}"
            next_level.append(hashlib.sha256(combined.encode()).hexdigest())

        return self._calculate_merkle_root(next_level)

    def _detect_timestamp_anomalies(self) -> List[Dict[str, Any]]:
        """Detect suspicious timestamp patterns."""
        anomalies = []

        # Get logs ordered by ID
        logs = self.db.query(AuditLog).order_by(AuditLog.id).all()

        for i in range(1, len(logs)):
            current_log = logs[i]
            previous_log = logs[i - 1]

            # Check for timestamp going backwards
            if current_log.timestamp < previous_log.timestamp:
                anomalies.append(
                    {
                        "log_id": current_log.id,
                        "type": "timestamp_regression",
                        "current_timestamp": current_log.timestamp.isoformat(),
                        "previous_timestamp": previous_log.timestamp.isoformat(),
                    }
                )

            # Check for suspicious gaps
            time_diff = (current_log.timestamp - previous_log.timestamp).total_seconds()
            if time_diff > 86400:  # More than 24 hours
                anomalies.append(
                    {
                        "log_id": current_log.id,
                        "type": "large_time_gap",
                        "gap_seconds": time_diff,
                    }
                )

        return anomalies

    def _detect_duplicate_hashes(self) -> List[Dict[str, Any]]:
        """Detect duplicate hash values."""
        from sqlalchemy import func

        duplicates = (
            self.db.query(AuditLog.hash_value, func.count(AuditLog.id).label("count"))
            .group_by(AuditLog.hash_value)
            .having(func.count(AuditLog.id) > 1)
            .all()
        )

        duplicate_details = []
        for hash_value, count in duplicates:
            logs_with_hash = (
                self.db.query(AuditLog).filter(AuditLog.hash_value == hash_value).all()
            )

            duplicate_details.append(
                {
                    "hash_value": hash_value,
                    "occurrence_count": count,
                    "log_ids": [log.id for log in logs_with_hash],
                }
            )

        return duplicate_details

    def _detect_missing_logs(self) -> List[Dict[str, Any]]:
        """Detect gaps in log ID sequence."""
        from sqlalchemy import text

        # Find gaps in ID sequence
        result = self.db.execute(
            text(
                """
            SELECT id + 1 as gap_start,
                    (SELECT MIN(id) - 1 FROM monitoring_audit_logs WHERE id > t.id) as gap_end
            FROM monitoring_audit_logs t
            WHERE NOT EXISTS (SELECT 1 FROM monitoring_audit_logs WHERE id = t.id + 1)
            AND id < (SELECT MAX(id) FROM monitoring_audit_logs)
        """
            )
        )

        gaps = []
        for row in result:
            gaps.append(
                {
                    "gap_start": row.gap_start,
                    "gap_end": row.gap_end,
                    "missing_count": (
                        row.gap_end - row.gap_start + 1 if row.gap_end else 1
                    ),
                }
            )

        return gaps
