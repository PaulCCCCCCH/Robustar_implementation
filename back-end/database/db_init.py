from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = None


def init_db(app):
    global db
    db = SQLAlchemy()
    print("Initializing database ... ")
    with app.app_context():
        db.create_all()
