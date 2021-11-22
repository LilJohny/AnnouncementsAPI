from app import db


def delete_obj(obj: db.Model):
    db.session.delete(obj)
    db.session.commit()


def add_obj(obj: db.Model):
    db.session.add(obj)
    db.session.commit()
