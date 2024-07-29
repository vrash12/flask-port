from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the database instance globally, but without specific app
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'admin'  # Replace with a strong secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/blog_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   
    db.init_app(app)

    with app.app_context():
        # Import parts of our application
        from .routes import init_routes
        init_routes(app)

        # Optional: Create the database tables if they don't exist
        db.create_all()

    return app
