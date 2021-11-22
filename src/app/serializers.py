from app import flask_app
from flask_marshmallow import Marshmallow

marshmallow = Marshmallow(flask_app)


class AnnouncementSchema(marshmallow.Schema):
    class Meta:
        fields = ("id_", "title", "description", "ticket_price", "hosts")


class HostSchema(marshmallow.Schema):
    class Meta:
        fields = ("id_", "first_name", "last_name", "about")


announcement_schema = AnnouncementSchema()
announcements_schema = AnnouncementSchema(many=True)

host_schema = HostSchema()
hosts_schema = HostSchema(many=True)


def dump_announcement(announcement):
    dumped = announcement_schema.dump(announcement)
    if dumped["hosts"]:
        dumped["hosts"] = hosts_schema.dump(dumped["hosts"])
    return dumped


def dump_announcements(announcements):
    dumped = announcements_schema.dump(announcements)

    def map_announcement_hosts(dumped_announcement):
        dumped_announcement["hosts"] = hosts_schema.dump(dumped_announcement["hosts"])
        return dumped_announcement

    dumped = list(map(map_announcement_hosts, dumped))
    return dumped
