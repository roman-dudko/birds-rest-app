from flask import Flask
from handlers.routes import configure_routes
import sys

sys.path.append('../')

# Init app
app = Flask(__name__)

configure_routes(app)

# Run server
if __name__ == '__main__':
    app.run(debug=True)