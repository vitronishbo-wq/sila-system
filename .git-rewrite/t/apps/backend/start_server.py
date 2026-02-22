import os
import logging
import uvicorn

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("uvicorn")
    logger.setLevel(logging.DEBUG)

    # Print all environment variables
    print("Environment variables:")
    for key, value in os.environ.items():
        print(f"{key}={value}")

    # Try to set the port
    from config.settings import settings
    settings.PORT = "8000"
    settings.UVICORN_PORT = "8000"

    # Start the server
    print("Starting server with port 8000")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        log_config={
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": "%(levelprefix)s %(asctime)s %(message)s",
                    "use_colors": True,
                },
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                },
            },
            "loggers": {
                "uvicorn": {"handlers": ["default"], "level": "DEBUG"},
                "uvicorn.error": {"handlers": ["default"], "level": "DEBUG"},
                "uvicorn.access": {"handlers": ["default"], "level": "DEBUG"},
            },
        },
    )
