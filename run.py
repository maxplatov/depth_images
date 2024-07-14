import uvicorn
import uvloop

from app.app import create_app
from app.settings import SETTINGS

app = create_app(SETTINGS)

if __name__ == "__main__":
    uvloop.install()

    uvicorn.run(
        app="run:app",
        host=SETTINGS.app.host,
        port=SETTINGS.app.port,
        workers=SETTINGS.app.workers,
        log_config=None,
        loop="uvloop",
    )
