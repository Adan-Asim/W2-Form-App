from extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)


class W2Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    data = db.Column(db.JSON, nullable=False)


class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    w2_form_id = db.Column(db.Integer, db.ForeignKey("w2_form.id"), nullable=False)
    user_query = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.now())

    user = db.relationship("User", backref=db.backref("chat_histories", lazy=True))
    w2_form = db.relationship("W2Form", backref=db.backref("chat_histories", lazy=True))


def init_models(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
