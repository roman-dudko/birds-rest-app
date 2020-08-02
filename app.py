from flask import Flask
from handlers.routes import configure_routes

# Init app
app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ornithologist:ornithologist@localhost:5432/birds_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

configure_routes(app)

# Run server
if __name__ == '__main__':
    app.run(debug=True)