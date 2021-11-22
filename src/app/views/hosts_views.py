from flask import jsonify
from flask import request
from flask.blueprints import Blueprint

from app import db
from app.constants import OBLIGATORY_ID_ERROR_MESSAGE, SUCCESS_HOST_DELETED, \
    ERROR_HOST_DOES_NOT_EXIST
from app.db_utils import create_host
from app.models import Host
from app.obj_utils import delete_obj
from app.serializers import hosts_schema, host_schema

hosts_bp = Blueprint("hosts", __name__, url_prefix="/hosts")


@hosts_bp.route("/", methods=["GET"])
def get_hosts():
    hosts_list = Host.query.all()
    result = hosts_schema.dump(hosts_list)
    return jsonify(result)


@hosts_bp.route("get/<int:host_id>", methods=["GET"])
def get_host(host_id: int):
    host = Host.query.filter_by(id_=host_id).first()
    if host:
        result = host_schema.dump(host)
        return jsonify(result)
    else:
        return jsonify(message=ERROR_HOST_DOES_NOT_EXIST.format(id_=host_id)), 404


@hosts_bp.route("delete/<int:host_id>", methods=["DELETE"])
def remove_host(host_id: int):
    host = Host.query.filter_by(id_=host_id).first()
    if host:
        delete_obj(host)
        return jsonify(message=SUCCESS_HOST_DELETED.format(id_=host_id)), 202
    else:
        return jsonify(message=ERROR_HOST_DOES_NOT_EXIST.format(id_=host_id)), 404


@hosts_bp.route("/create", methods=["POST"])
def add_host():
    data = request.get_json()
    host_id, first_name, last_name, about = data.get("id_"), data.get("first_name", ""),\
                                            data.get("last_name", ""), data.get("about", "")

    host = create_host(host_id, first_name, last_name, about)
    result = host_schema.dump(host)
    return jsonify(mesaage=result), 201


@hosts_bp.route("/update", methods=["PUT"])
def update_host():
    data = request.get_json()
    host_id, first_name, last_name, about = data.get("id_"), data.get("first_name", ""),\
                                            data.get("last_name", ""), data.get("about", "")
    if not host_id:
        return jsonify(message=OBLIGATORY_ID_ERROR_MESSAGE), 400

    host = Host.query.filter_by(id_=host_id).first()
    if not host:
        return jsonify(message=ERROR_HOST_DOES_NOT_EXIST.format(id_=host_id)), 404

    host.first_name = first_name
    host.last_name = last_name
    host.about = about
    db.session.commit()
    result = host_schema.dump(host)

    return jsonify(message=result), 202
