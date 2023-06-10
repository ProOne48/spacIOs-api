from base.settings import settings

from src.app import app
from flask_cors import CORS

if __name__ == '__main__':
    CORS(app)
    app.debug = settings.DEBUG_MODE
    app.run(threaded=True)
