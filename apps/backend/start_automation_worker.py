#!/usr/bin/env python3
import logging
import signal
import time

from foundation.automation.automator import AutomationEngine

logging.basicConfig(level=logging.INFO, format="[automation] %(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Initializing automation worker")
    auto = AutomationEngine()
    stopped = False

    def shutdown(signum, frame):
        nonlocal stopped
        logger.info("Shutdown requested (%s)", signum)
        stopped = True

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    logger.info("Automation worker started and listening for transfer events")
    try:
        while not stopped:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("Stopping automation worker")
        try:
            auto.stop()
        except Exception:
            logger.exception("Failed to stop automation engine cleanly")


if __name__ == "__main__":
    main()
