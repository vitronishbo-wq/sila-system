import logging

logger = logging.getLogger("national_soc")


class SOCMonitor:
    """National SOC (Security Operations Center) monitoring"""

    def threat(self, message):
        """Log critical threat"""
        logger.critical(f"THREAT {message}")

    def anomaly(self, message):
        """Log anomalous behavior"""
        logger.warning(f"ANOMALY {message}")

    def fraud(self, message):
        """Log suspected fraud"""
        logger.error(f"FRAUD {message}")
