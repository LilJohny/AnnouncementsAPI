from flask import jsonify, request
from flask.blueprints import Blueprint

from app import db
from app.constants import OBLIGATORY_ID_ERROR_MESSAGE, \
    SUCCESS_ANNOUNCEMENT_DELETED, ERROR_ANNOUNCEMENT_DOES_NOT_EXIST
from app.db_utils import get_hosts_by_id, create_announcement
from app.models import Announcement
from app.obj_utils import delete_obj
from app.serializers import announcement_schema, dump_announcement, \
    dump_announcements
from app.validators import validate_str_float, validate_str_datetime

announcements_bp = Blueprint("announcements", __name__, url_prefix="/announcements")


@announcements_bp.route("/delete/<int:announcement_id>", methods=["DELETE"])
def remove_announcement(announcement_id: int):
    announcement = Announcement.query.filter_by(id_=announcement_id).first()
    if announcement:
        delete_obj(announcement)
        return jsonify(message=SUCCESS_ANNOUNCEMENT_DELETED.format(id_=announcement_id)), 202
    else:
        return jsonify(message=ERROR_ANNOUNCEMENT_DOES_NOT_EXIST.format(id_=announcement_id)), 404


@announcements_bp.route("/", methods=["GET"])
def get_announcements():
    announcements_list = Announcement.query.all()
    dumped_announcements = dump_announcements(announcements_list)
    return jsonify(dumped_announcements)


@announcements_bp.route("/get/<int:announcement_id>", methods=["GET"])
def get_announcement(announcement_id: int):
    announcement = Announcement.query.filter_by(id_=announcement_id).first()
    if announcement:
        result = announcement_schema.dump(announcement)
        return jsonify(result.data)
    else:
        return jsonify(message=ERROR_ANNOUNCEMENT_DOES_NOT_EXIST.format(id_=announcement_id)), 404


@announcements_bp.route("/create", methods=["POST"])
def add_announcement():
    data = request.get_json()
    announcement_id, title, description, date_time, location, ticket_price = data.get("id_"), \
                                                                             data.get("title"), \
                                                                             data.get("description"), \
                                                                             data.get("datetime"), \
                                                                             data.get("location"), \
                                                                             data.get("ticket_price")

    errors = []

    validate_str_float(ticket_price, errors)
    validate_str_datetime(date_time, errors)

    if len(errors):
        return jsonify(message=errors), 403

    hosts = data.get("hosts")

    if hosts:
        hosts = get_hosts_by_id(hosts)

    announcement = create_announcement(announcement_id, title, description, date_time, location, ticket_price, hosts)
    dumped_announcement = dump_announcement(announcement)
    return jsonify(message=dumped_announcement), 201


@announcements_bp.route("/update", methods=["PUT"])
def update_announcement():
    data = request.get_json()
    announcement_id, title, description, date_time, location, ticket_price = data.get("id_"), \
                                                                             data.get("title"), \
                                                                             data.get("description"), \
                                                                             data.get("datetime"), \
                                                                             data.get("location"), \
                                                                             data.get("ticket_price")
    if not announcement_id:
        return jsonify(message=OBLIGATORY_ID_ERROR_MESSAGE), 400
    errors = []

    validate_str_float(ticket_price, errors)
    validate_str_datetime(date_time, errors)

    if len(errors):
        return jsonify(message=errors), 403

    hosts = data.get("hosts")

    if hosts:
        hosts = get_hosts_by_id(hosts)
    else:
        hosts = []

    announcement = Announcement.query.filter_by(id_=announcement_id).first()
    announcement.id_ = announcement_id
    announcement.title = title
    announcement.description = description
    announcement.date_time = date_time
    announcement.location = location
    announcement.ticket_price = ticket_price
    announcement.hosts = hosts
    db.session.commit()
    dumped_announcement = dump_announcement(announcement)

    return jsonify(message=dumped_announcement), 202
