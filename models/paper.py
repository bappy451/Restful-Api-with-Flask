from db import db


class PaperModel(db.Model):
    __tablename__ = 'papers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    journalName = db.Column(db.String(256))
    area = db.Column(db.String())
    abstract = db.Column(db.String())
    fullPaper = db.Column(db.String())

    authors = db.relationship('AuthorModel', lazy='dynamic')

    def __init__(self, name,  journalName, area, abstract, fullPaper):
        self.name = name
        self.journalName = journalName
        self.area = area
        self.abstract = abstract
        self.fullPaper = fullPaper
        
    def json(self):
        return {'name': self.name, 'journalName':self.journalName, 'abstract':self.abstract, 'fullPaper':self.fullPaper, 'area':self.area, 'authors': [author.json() for author in self.authors.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
