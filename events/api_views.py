import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from encoders import (ConferenceDetailEncoder, ConferenceListEncoder,
                      LocationDetailEncoder, LocationListEncoder)

from .acl import get_coord, get_image, get_weather
from .models import Conference, Location, State

# from json import JSONEncoder
# from common.json import ModelEncoder

@require_http_methods(["GET", "POST"])
def api_list_conferences(request):
    """
    Lists the conference names and the link to the conference.

    Returns a dictionary with a single key "conferences" which
    is a list of conference names and URLS. Each entry in the list
    is a dictionary that contains the name of the conference and
    the link to the conference's information.

    {
        "conferences": [
            {
                "name": conference's name,
                "href": URL to the conference,
            },
            ...
        ]
    }
    """
    # get model instances given specific id
    conferences = Conference.objects.all()

    # Get a list of all of the instances of «resource»
    if request.method == "GET":
        # return json with instance parameters serialized to json
        return JsonResponse(
            # conferences,  # also works
            {"conferences": conferences},
            encoder=ConferenceListEncoder,
            safe=False,
        )

    # Create a new instance of «resource» with the posted data
    else:  # POST

        # create a conference
        content = json.loads(request.body)

        # Get the Location object and put it in the content dict
        try:
            location = Location.objects.get(id=content["location"])
            content["location"] = location
        except Location.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid location id"},
                status=400,
            )

        conference = Conference.objects.create(**content)
        return JsonResponse(
            conference,
            encoder=ConferenceDetailEncoder,
            safe=False,
        )

    # response = []
    # conferences = Conference.objects.all()
    # for conference in conferences:
    #     response.append(
    #         {
    #             "name": conference.name,
    #             "href": conference.get_api_url(),
    #         }
    #     )
    # return JsonResponse({"conferences": response})


@require_http_methods({"GET", "DELETE", "PUT"})
def api_show_conference(request, pk):
    """
    Returns the details for the Conference model specified
    by the pk parameter.

    This should return a dictionary with the name, starts,
    ends, description, created, updated, max_presentations,
    max_attendees, and a dictionary for the location containing
    its name and href.

    {
        "name": the conference's name,
        "starts": the date/time when the conference starts,
        "ends": the date/time when the conference ends,
        "description": the description of the conference,
        "created": the date/time when the record was created,
        "updated": the date/time when the record was updated,
        "max_presentations": the maximum number of presentations,
        "max_attendees": the maximum number of attendees,
        "location": {
            "name": the name of the location,
            "href": the URL for the location,
        }
    }
    """
    if request.method == "GET":
        # get model instance given specific id
        conference = Conference.objects.get(id=pk)

        # get city, state from conference
        city = conference.location.city
        state = conference.location.state

        # get coords
        lat, lon = get_coord(city, state.name)

        # get weather data
        if lat and lon:
            weather = get_weather(lat, lon)
        else:
            weather = None

        # return json with instance parameters serialized to json
        # include weather data in jsonresponse (not in db instance)
        return JsonResponse(
            {"conference": conference, "weather": weather},
            encoder=ConferenceDetailEncoder,
            # encoder will only act on conference model instances
            safe=False,
        )

    elif request.method == "DELETE":
        count, _ = Conference.objects.filter(id=pk).delete()

        return JsonResponse(
            {"deleted": count > 0},
        )

    else:
        content = json.loads(request.body)

        try:
            if "location" in content:
                location = Location.objects.get(id=content["location"])
                content["location"] = location
        except Location.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid location id"},
                status=400,
            )

        Conference.objects.filter(id=pk).update(**content)
        conference = Conference.objects.get(id=pk)

        return JsonResponse(
            conference,
            encoder=ConferenceDetailEncoder,
            safe=False,
        )

    # encoder handles conversion
    # safe = False allows other serialized form of data
    # (function requires dictionary)

    # DOESN'T WORK
    # return JsonResponse(conference)


@require_http_methods(["GET", "POST"])
def api_list_locations(request):
    """
    Lists the location names and the link to the location.

    Returns a dictionary with a single key "locations" which
    is a list of location names and URLS. Each entry in the list
    is a dictionary that contains the name of the location and
    the link to the location's information.

    {
        "locations": [
            {
                "name": location's name,
                "href": URL to the location,
            },
            ...
        ]
    }
    """

    locations = Location.objects.all()

    # if Gets a list of all of the instances of «resource»
    if request.method == "GET":
        return JsonResponse(
            # locations,
            {"locations": locations},
            encoder=LocationListEncoder,
            safe=False,
        )

    # if Create a new instance of «resource» with the posted data
    elif request.method == "POST":

        # 1. Decode JSON into dict
        # create a location
        content = json.loads(request.body)

        # get the city and state from content
        city = content["city"]
        state = content["state"]

        # get image
        image_url = get_image(city, state)

        # add image to new model (need to add field to actual
        # location model first)
        content["image_url"] = image_url

        # Get the State object and put it in the content dict
        try:
            # 2. Translate properties into model objects
            state = State.objects.get(abbreviation=content["state"])
            content["state"] = state

        # 3. Handle any errors that could happen
        except State.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid state abbreviation"},
                status=404,
            )

        # 4. Create new Entity instance
        location = Location.objects.create(**content)  # TODO - understand

        # 5. Return new entity in JsonResponse
        return JsonResponse(
            location, encoder=LocationDetailEncoder, safe=False
        )


@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_location(request, pk):
    """
    Returns the details for the Location model specified
    by the pk parameter.

    This should return a dictionary with the name, city,
    room count, created, updated, and state abbreviation.

    {
        "name": location's name,
        "city": location's city,
        "room_count": the number of rooms available,
        "created": the date/time when the record was created,
        "updated": the date/time when the record was updated,
        "state": the two-letter abbreviation for the state,
    }
    """

    # if Gets the details of one instance of «resource»
    if request.method == "GET":
        location = Location.objects.get(id=pk)
        return JsonResponse(
            location, encoder=LocationDetailEncoder, safe=False
        )

    elif request.method == "DELETE":
        count, _ = Location.objects.filter(id=pk).delete()
        # per docs, delete() returns # objects deleted, dict
        # with # del per object type
        return JsonResponse({"deleted": count > 0})

    # if Updates the details of one instance of «resource» (PUT)
    elif request.method == "PUT":
        # 1. Convert the submitted JSON-formatted string into a dictionary.
        content = json.loads(request.body)

        # get the city and state from content
        city = content["city"]
        state = content["state"]

        # get image
        image_url = get_image(city, state)

        # add image to new model (need to add field to actual
        # location model first)
        content["image_url"] = image_url

        # 2. Convert the state abbreviation into a State, if it exists.
        try:
            if "state" in content:
                state = State.objects.get(abbreviation=content["state"])
                content["state"] = state
        except State.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid state abbreviation"},
                status=400,
            )

        # 3. Use that dictionary to update the existing Location.
        Location.objects.filter(id=pk).update(**content)
        # .update(**content) inserts content into instance of model

        # 4. Return the updated Location object.
        location = Location.objects.get(id=pk)
        return JsonResponse(
            location,
            encoder=LocationDetailEncoder,
            safe=False,
        )
