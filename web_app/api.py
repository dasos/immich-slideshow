import requests
import datetime
import random

from flask import Blueprint, current_app, make_response
from urllib.parse import urlparse


bp = Blueprint("api", __name__, url_prefix="/api")


def request_wrap(url, params=None):
    immich_server = current_app.config.get("IMMICH_SERVER")
    api_key = current_app.config.get("IMMICH_API_KEY")
    # search_query = current_app.config.get("SEARCH_QUERY")

    immich_parsed_url = urlparse(immich_server)
    base_url = f"{immich_parsed_url.scheme}://{immich_parsed_url.netloc}"
    api_url = f"{base_url}/api"

    headers = {"x-api-key": api_key}

    return requests.get(api_url + url, headers=headers, params=params)


@bp.route("/photos")
def get_photos():

    current_time = datetime.datetime.now()

    params = {"day": current_time.day, "month": current_time.month}

    response = request_wrap("/asset/memory-lane", params)

    # return json.dumps(response.json(), indent=2)

    # Remove the stuff we don't need
    asset_list = [
        {"id": y["id"], "datetime": y["localDateTime"]}
        for x in response.json()
        for y in x["assets"]
    ]
    random.shuffle(asset_list)

    return asset_list


@bp.route("/proxy/<string:id>")
def proxy(id):

    r = request_wrap(f"/asset/thumbnail/{id}?format=JPEG")

    response = make_response(r.content)
    response.content_type = r.headers.get("content-type")
    return response
