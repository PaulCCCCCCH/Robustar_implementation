from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    print("Initializing database ... ")
    with app.app_context():
        db.create_all()
