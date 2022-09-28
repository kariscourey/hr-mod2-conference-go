from events.models import Conference, Location
from presentations.models import Presentation
from common.json import ModelEncoder


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
    ]  # defines what part of a conference we actually want to convert into json
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
    ]

    # override get_extra_data of class def
    def get_extra_data(self, o):
        # return populated to dict (to update d with in ModelEncoder)
        return {"status": o.status.name}