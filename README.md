
# Immich Slideshow

Immich Slideshow is a Python3 web app that displays photos from Immich in a rotating slideshow. It is to be used on an old tablet, letting you see photos you may otherwise miss. The code used to display the photos targets old versions of webview, which means the CSS and JavaScript is very old and basic.

## Warning!

This code includes a reverse proxy of sorts, which reserves the photo. This is to avoid CORS issues, and also reduce authentication issues. However, it means anyone can see a photo, without an API key, as long as they know the ID. This is obviously very insecure. Do not expose this to the web!

## Development, or local install

### Dependancies
Python 3, plus the modules in requirements.txt

### How to run a development server
Assumption is a Ubuntu machine.

Create your virtual environment

    python3 -m venv venv
    source venv/bin/activate

Install the dependancies:

    pip3 install -r requirements.txt

Set the variables:

    export iimich_key=<abc123>
    export FLASK_DEBUG=true

Execute:

    python3 web_app/app.py

### Code standards

Auto-formatting is achieved using Black:

    python3 -m black .

And making sure PEP 8 is followed is done with Flake8, with the adjustments that Black recommend.

    python3 -m flake8 .