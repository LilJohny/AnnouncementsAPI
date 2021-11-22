from app import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

association_table = Table('association', db.metadata,
                          Column('announcementsid_', ForeignKey('announcements.id_')),
                          Column('hostsid_', ForeignKey('hosts.id_'))
                          )


class Announcement(db.Model):
    __tablename__ = "announcements"
    id_ = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    date_time = Column(String)
    location = Column(String)
    ticket_price = Column(Float)
    hosts = relationship("Host", secondary=association_table)


class Host(db.Model):
    __tablename__ = "hosts"
    id_ = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    about = Column(String)
