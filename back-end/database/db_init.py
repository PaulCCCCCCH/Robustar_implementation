from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
import os
from utils.path_utils import to_absolute

db = SQLAlchemy()


def init_db(app, db_path):
    db_conn_str = f"sqlite:///{to_absolute(os.getcwd(), db_path)}"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_conn_str

    db.init_app(app)

    engine = sa.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    inspector = sa.inspect(engine)
    if not inspector.has_table("models"):
        with app.app_context():
            db.drop_all()
            db.create_all()

    # print("Initializing database ... ")
    # with app.app_context():
    #     db.create_all()
