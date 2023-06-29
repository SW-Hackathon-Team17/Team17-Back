from app import db

class Form(db.Model):
    frormIdx = db.Column(db.Integer,primary_key =True)
    
class Presentation(db.Model):
    pptIdx=db.Column(db.Integer, primary_key=True)
    formIdx = db.Column(db.Integer, db.ForeignKey(
        'form.id', ondelete='CASCADE'))
    form = db.relationship(
        'Form', backref=db.backref('form_set'))
    
class ScriptOnly(db.Model):
    scriptOnlyIdx=db.Column(db.Integer, primary_key=True)
    formIdx = db.Column(db.Integer, db.ForeignKey(
        'form.id', ondelete='CASCADE'))
    form = db.relationship(
        'Form', backref=db.backref('form_set'))
    script = db.Column(db.Text, nullable=False)
    
class Image(db.Model):
    imgIdx = db.Column(db.Integer, primary_key=True)
    pptIdx = db.Column(db.Integer, db.ForeignKey(
        'presentation.id', ondelete='CASCADE'))
    presentation = db.relationship(
        'Presentation', backref=db.backref('ppt_set'))
    pgNum = db.Column(db.Integer, nullable=False)
    imgUrl = db.Column(db.Text, nullable=False)
    script = db.Column(db.Text)
    
class KeyWord(db.Model):
    keyIdx=db.Column(db.Integer, primary_key=True)
    keyWord = db.Column(db.String(45), nullable=False)
    imgIdx = db.Column(db.Integer, db.ForeignKey(
        'image.id', ondelete='CASCADE'))
    image = db.relationship(
        'Image', backref=db.backref('img_set'))
    level = db.Column(db.Integer, nullable=False, default=0) #0 :default , 1 :중요도1 , 2 :중요도2
    scriptOnlyIdx = db.Column(db.Integer, db.ForeignKey(
        'scriptOnly.id', ondelete='CASCADE'))
    script = db.relationship(
        'ScriptOnly', backref=db.backref('scriptOnly_set')
    )
    
    
    
    

