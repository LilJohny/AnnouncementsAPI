from app import db
from app.models import Host
from app.obj_utils import add_obj


def create_host(host_id, first_name, last_name, about):
    if host_id:
        host = Host.query.filter_by(id_=host_id).first()
        if not host and first_name and last_name:
            host = Host(id_=host_id, first_name=first_name, last_name=last_name, about=about)
            add_obj(host)
    else:
        host = Host(first_name=first_name, last_name=last_name, about=about)
        add_obj(host)
    return host


def get_hosts_by_id(ids: list):
    hosts = db.session.query(Host).filter(Host.id_.in_(ids)).all()
    return hosts
