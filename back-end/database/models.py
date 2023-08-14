from objects.RDataManager import db


class EvalResults(db.Model):
    model_id = db.Column(db.BigInteger, primary_key=True)
    img_path = db.Column(db.String, primary_key=True)
    result = db.Column(db.Integer)


# Many-to-many relationship reference
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
influ_rel = db.Table(
    "influ_rel",
    db.Column("model_id", db.BigInteger, db.ForeignKey("models.id"), primary_key=True),
    db.Column(
        "image_path", db.Integer, db.ForeignKey("test_set.path"), primary_key=True
    ),
    db.Column("influ_path", db.Integer),
)


class Models(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    architecture = db.Column(db.String)
    tags = db.Column(db.String)
    create_time = db.Column(db.DateTime)
    weight_path = db.Column(db.String)
    code_path = db.Column(db.String)
    epoch = db.Column(db.Integer)
    train_accuracy = db.Column(db.Float)
    val_accuracy = db.Column(db.Float)
    test_accuracy = db.Column(db.Float)
    last_eval_on_dev_set = db.Column(db.DateTime)
    last_eval_on_test_set = db.Column(db.DateTime)

    influences = db.relationship(
        "TestSet",
        secondary=influ_rel,
        lazy="subquery",
        backref=db.backref("models", lazy=True),
    )


class PairedSet(db.Model):
    path = db.Column(db.String, primary_key=True)
    train_path = db.Column(db.String)


class Proposed(db.Model):
    path = db.Column(db.String, primary_key=True)
    train_path = db.Column(db.String)


class TestSet(db.Model):
    path = db.Column(db.String, primary_key=True)


class TrainSet(db.Model):
    path = db.Column(db.String, primary_key=True)
    paired_path = db.Column(db.String, db.ForeignKey("paired_set.path"))


class ValSet(db.Model):
    path = db.Column(db.String, primary_key=True)


class Visuals(db.Model):
    visual_path = db.Column(db.String, primary_key=True, unique=True)

    # TODO: Cannot set foreign key for image_path
    # because this can refer to train/val/test table.
    # Maybe consider merging those tables together?
    image_path = db.Column(db.String)
    model_id = db.Column(db.BigInteger, db.ForeignKey("models.id"))
