import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from encoders import AttendeeDetailEncoder, AttendeeListEncoder
from events.models import Conference

from .models import Attendee


@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_id):
    """
    Lists the attendees names and the link to the attendee
    for the specified conference id.

    Returns a dictionary with a single key "attendees" which
    is a list of attendee names and URLS. Each entry in the list
    is a dictionary that contains the name of the attendee and
    the link to the attendee's information.

    {
        "attendees": [
            {
                "name": attendee's name,
                "href": URL to the attendee,
            },
            ...
        ]
    }
    """
    # get model instances given specific id
    attendees = Attendee.objects.filter(conference=conference_id)

    if request.method == "GET":
        # return json with instance parameters serialized to json
        return JsonResponse(
            {"attendees": attendees},
            encoder=AttendeeListEncoder,
            safe=False,
        )

    elif request.method == "POST":
        content = json.loads(request.body)

        try:
            conference = Conference.objects.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )

        attendees = Attendee.objects.create(**content)
        return JsonResponse(
            {"attendees": attendees},
            encoder=AttendeeDetailEncoder,
            safe=False,
        )

    # attendees = [
    #     {
    #         "name": a.name,
    #         "href": a.get_api_url(),
    #     }
    #     for a in Attendee.objects.filter(conference=conference_id)
    # ]

    # return JsonResponse({"attendees": attendees})


@require_http_methods(["GET", "DELETE", "PUT"])
def api_show_attendee(request, pk):
    """
    Returns the details for the Attendee model specified
    by the pk parameter.

    This should return a dictionary with email, name,
    company name, created, and conference properties for
    the specified Attendee instance.

    {
        "email": the attendee's email,
        "name": the attendee's name,
        "company_name": the attendee's company's name,
        "created": the date/time when the record was created,
        "conference": {
            "name": the name of the conference,
            "href": the URL to the conference,
        }
    }
    """
    if request.method == "GET":
        # get model instance given specific id
        attendee = Attendee.objects.get(id=pk)

        # return json with instance parameters serialized to json
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )

    elif request.method == "DELETE":
        count, _ = Attendee.objects.filter(id=pk).delete()
        return JsonResponse(
            {"deleted": count > 0}
        )

    elif request.method == "PUT":
        content = json.loads(request.body)
        Attendee.objects.filter(id=pk).update(**content)

        attendee = Attendee.objects.get(id=pk)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )



    # attendee = Attendee.objects.get(id=pk)

    # return JsonResponse(
    #     {
    #         "email": attendee.email,
    #         "name": attendee.name,
    #         "company_name": attendee.company_name,
    #         "created": attendee.created,
    #         "conference": {
    #             "name": attendee.conference.name,
    #             "href": attendee.conference.get_api_url(),
    #         },
    #     }
    # )
