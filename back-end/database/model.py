from .db_init import db


class EvalResults(db.Model):
    model_id = db.Column(db.BigInteger, primary_key=True)
    img_path = db.Column(db.String, primary_key=True)
    result = db.Column(db.Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# Many-to-many relationship reference
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
influ_rel = db.Table(
    "influ_rel",
    db.Column("model_id", db.BigInteger, db.ForeignKey("models.id"), primary_key=True),
    db.Column(
        "image_path", db.Integer, db.ForeignKey("test_set_image.path"), primary_key=True
    ),
    db.Column("influ_path", db.Integer),
)
model_tag_rel = db.Table(
    "model_tag_rel",
    db.Column("model_id", db.Integer, db.ForeignKey("models.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


class Models(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_name = db.Column(db.String)
    nickname = db.Column(db.String)
    predefined = db.Column(db.Boolean)
    pretrained = db.Column(db.Boolean)
    description = db.Column(db.String)
    architecture = db.Column(db.String)
    tags = db.relationship("Tags", secondary=model_tag_rel, backref="models")
    create_time = db.Column(db.DateTime)
    weight_path = db.Column(db.String)
    code_path = db.Column(db.String)
    epoch = db.Column(db.Integer)
    train_accuracy = db.Column(db.Float)
    val_accuracy = db.Column(db.Float)
    test_accuracy = db.Column(db.Float)
    # If model is uploaded but not trained, last_trained should be empty
    # otherwise it will be the same as create_time
    last_trained = db.Column(db.DateTime)
    last_eval_on_dev_set = db.Column(db.DateTime)
    last_eval_on_test_set = db.Column(db.DateTime)

    influences = db.relationship(
        "TestSetImage",
        secondary=influ_rel,
        lazy="subquery",
        backref=db.backref("models", lazy=True),
    )

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data["tags"] = [tag.name for tag in self.tags]
        return data



class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class PairedSetImage(db.Model):
    path = db.Column(db.String, primary_key=True)
    train_path = db.Column(db.String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ProposedImage(db.Model):
    path = db.Column(db.String, primary_key=True)
    train_path = db.Column(db.String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TestSetImage(db.Model):
    path = db.Column(db.String, primary_key=True)
    label = db.Column(db.Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TrainSetImage(db.Model):
    path = db.Column(db.String, primary_key=True)
    paired_path = db.Column(db.String, db.ForeignKey("paired_set_image.path"))
    label = db.Column(db.Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ValSetImage(db.Model):
    path = db.Column(db.String, primary_key=True)
    label = db.Column(db.Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Visuals(db.Model):
    visual_path = db.Column(db.String, primary_key=True, unique=True)

    # TODO: Cannot set foreign key for image_path
    # because this can refer to train/val/test table.
    # Maybe consider merging those tables together?
    image_path = db.Column(db.String)
    model_id = db.Column(db.BigInteger, db.ForeignKey("models.id"))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
