from django.http import HttpResponse
import json


def generate_error(context, status_code):
    response = HttpResponse(
        json.dumps(context),
        content_type="application/json",
    )
    response.status_code = status_code
    return response
