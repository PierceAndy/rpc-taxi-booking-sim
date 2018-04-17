from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from json import JSONDecodeError
from . import models


@require_POST
@csrf_exempt
def book(request):
    """Books nearest available taxi, given customer location and destination.

    Booking is successful if
        - there are taxis available,
        - the provided location and destination are different
        - HttpRequest made with HTTP POST request
        - HttpRequest content-type is "application/json"
        - HttpRequest JSON data is correct and can be parsed

    Args:
        request: A HttpRequest instance.
            Content-Type: application/json
            Content: JSON containing customer location and destination, e.g.
                {"source": {"x": 1, "y": 2}, "destination": {"x": 1, "y": 2}}

    Returns:
        HttpResponse instance.
            If booking is successful:
                Status code: 200
                Content: JSON containing taxi ID and total travel time needed,
                    e.g. {"car_id": 1, "total_time": 7}
            If booking is unsuccessful:
                Status code: 204
                Content: Empty
            If HttpRequest content-type is wrong:
                Status code: 415
                Content: Text detailing expected and received content-types
            If JSON data cannot be parsed:
                Status code: 400
                Content: Text on error encountered when decoding JSON data
    """
    if request.content_type != "application/json":
        return HttpResponse("Expected Content-Type: application/json\n"
                            + "Received Content-Type: {}".format(request.content_type),
                            status=415)
    try:
        booking = json.loads(request.body, encoding=request.encoding)
    except JSONDecodeError:
        return HttpResponseBadRequest("Error decoding JSON data")

    response = models.make(booking)
    if not response:
        return HttpResponse(status=204)
    else:
        return JsonResponse(response)


@require_POST
@csrf_exempt
def tick(request):
    """Advances service time stamp by one unit.

    Advancement is successful if
        - HttpRequest made with HTTP POST request

    Args:
        request: A HttpRequest instance.

    Returns:
        HttpResponse instance.
            Status code: 204
            Content: Empty
    """
    models.increment_time()
    return HttpResponse(status=204)


@require_POST
@csrf_exempt
def reset(request):
    """Resets all taxis to initial state regardless of availability.

    Advancement is successful if
        - HttpRequest made with HTTP POST request

    Args:
        request: A HttpRequest instance.

    Returns:
        HttpResponse instance.
            Status code: 204
            Content: Empty
    """
    models.reset()
    return HttpResponse(status=204)
