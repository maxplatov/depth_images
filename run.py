import uvicorn
import uvloop

from app.app import create_app
from app.settings import SETTINGS

app = create_app(SETTINGS)


if __name__ == "__main__":
    uvloop.install()
    settings = SETTINGS

    uvicorn.run(
        app="run:app",
        host=settings.app.host,
        port=settings.app.port,
        workers=settings.app.workers,
        log_config=None,
        loop="uvloop",
    )
