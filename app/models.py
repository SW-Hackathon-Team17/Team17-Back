from app import db


class Form(db.Model):
    formIdx = db.Column(db.Integer, primary_key=True)
    presentation = db.relationship(
        'Presentation', backref=db.backref('form_set'))
    scriptonly = db.relationship(
        'Scriptonly', backref=db.backref('form_set'))


class Presentation(db.Model):
    pptIdx = db.Column(db.Integer, primary_key=True)
    formIdx = db.Column(db.Integer, db.ForeignKey(
        'form.formIdx', ondelete='CASCADE'))
    image = db.relationship(
        'Image', backref=db.backref('presentation_set'))


class Scriptonly(db.Model):
    scriptOnlyIdx = db.Column(db.Integer, primary_key=True)
    formIdx = db.Column(db.Integer, db.ForeignKey(
        'form.formIdx', ondelete='CASCADE'))
    keyword = db.relationship(
        'Keyword', backref=db.backref('scriptonly_set'))
    script = db.Column(db.Text, nullable=False)


class Image(db.Model):
    imgIdx = db.Column(db.Integer, primary_key=True)
    pptIdx = db.Column(db.Integer, db.ForeignKey(
        'presentation.pptIdx', ondelete='CASCADE'))
    keyword = db.relationship(
        'Keyword', backref=db.backref('image_set'))
    pgNum = db.Column(db.Integer, nullable=False)
    imgUrl = db.Column(db.Text, nullable=False)
    script = db.Column(db.Text)
    topic = db.Column(db.Integer)


class Keyword(db.Model):
    keyIdx = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(45), nullable=False)
    imgIdx = db.Column(db.Integer, db.ForeignKey(
        'image.imgIdx', ondelete='CASCADE'))
    # 0 :default , 1 :중요도1 , 2 :중요도2
    level = db.Column(db.Integer, nullable=False, default=0)
    scriptOnlyIdx = db.Column(db.Integer, db.ForeignKey(
        'scriptonly.scriptOnlyIdx', ondelete='CASCADE'))
    topic = db.Column(db.Integer)
