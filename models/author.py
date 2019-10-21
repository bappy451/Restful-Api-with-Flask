from db import db


class AuthorModel(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    institutin_name = db.Column(db.String())
    email = db.Column(db.String())
    designation = db.Column(db.String())

    paper_id = db.Column(db.Integer, db.ForeignKey('papers.id'))
    paper = db.relationship('PaperModel')

    def __init__(self, name, institutin_name, paper_id, email, designation):
        self.name = name
        self.institutin_name = institutin_name
        self.paper_id = paper_id
        self.email = email
        self.designation = designation

    def json(self):
        return {'name': self.name, 'institutin_name': self.institutin_name, 'email':self.email, 'designation': self.designation}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
