from attendees.models import Attendee
from common.json import ModelEncoder
from events.models import Conference, Location
from presentations.models import Presentation


class LocationListEncoder(ModelEncoder):
    model = Location
    properties = [
        "name",
    ]


class LocationDetailEncoder(ModelEncoder):
    model = Location
    properties = [
        "name",
        "city",
        "room_count",
        "created",
        "updated",
        "state",
        "image_url",
    ]

    # override get_extra_data of class def
    def get_extra_data(self, o):
        # return populated to dict (to update d with in ModelEncoder)
        return {"state": o.state.abbreviation}


class ConferenceListEncoder(ModelEncoder):
    model = Conference
    properties = [
        "name",
    ]


class ConferenceDetailEncoder(ModelEncoder):
    model = Conference
    properties = [
        "name",
        "starts",
        "ends",
        "description",
        "created",
        "updated",
        "max_presentations",
        "max_attendees",
        "location",
    ]
    # defines what part of a conference we actually want
    # to convert into json
    encoders = {
        "location": LocationListEncoder(),
    }


class PresentationListEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "title",
        "status",
    ]

    # override get_extra_data of class def
    def get_extra_data(self, o):
        # return populated to dict (to update d with in ModelEncoder)
        return {"status": o.status.name}


class PresentationDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
        "status",
        "conference",
    ]
    encoders = {
        "conference": ConferenceListEncoder(),
    }

    # override get_extra_data of class def
    def get_extra_data(self, o):
        # return populated to dict (to update d with in ModelEncoder)
        return {"status": o.status.name}


class AttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "name",
    ]


class AttendeeDetailEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "email",
        "name",
        "company_name",
        "created",
        "conference",
    ]
    encoders = {
        "conference": ConferenceListEncoder(),
    }
