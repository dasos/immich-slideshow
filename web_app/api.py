import requests
from datetime import datetime, timedelta
import random

import json

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

    response = requests.get(api_url + url, headers=headers, params=params)
    
    if (response.status_code != 200):
      print (json.dumps(response.json(), indent=2))
      raise Exception("Probably not authorised, or API has changed")
    
    return response


@bp.route("/photos")
def get_photos():
    count = 0
    asset_list = []
    while len(asset_list) < 20 and count < 7:
        asset_list = asset_list + _get_photos(count)
        print(f"Current asset length: {len(asset_list)}")
        count = count + 1

    return asset_list


def _get_photos(day_adjust=0):

    current_time = datetime.now()
    dt = current_time + timedelta(days=day_adjust)

    params = {"day": dt.day, "month": dt.month}

    response = request_wrap("/assets/memory-lane", params)

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

    r = request_wrap(f"/assets/{id}/thumbnail?size=preview")

    response = make_response(r.content)
    response.content_type = r.headers.get("content-type")
    return response
