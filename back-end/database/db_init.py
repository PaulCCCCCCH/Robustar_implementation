from flask_sqlalchemy import SQLAlchemy


def create_sqlalchemy_db(app):
    with app.app_context():
        db = SQLAlchemy(app)
        return db

def init_db(app, db):
    print("Initializing database ... ")
    with app.app_context():
        db.create_all()
