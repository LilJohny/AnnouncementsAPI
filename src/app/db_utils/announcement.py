from app.models import Announcement
from app.obj_utils import add_obj


def create_announcement(announcement_id, title, description, date_time, location,
                        ticket_price, hosts=None):
    if announcement_id:
        announcement = Announcement.query.filter_by(id_=announcement_id).first()
        if announcement:
            return announcement
    hosts = [] if hosts is None else hosts
    announcement = Announcement(title=title, description=description, date_time=date_time, location=location,
                                ticket_price=ticket_price, hosts=hosts)
    add_obj(announcement)
    return announcement
