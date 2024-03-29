import logging
from flask import Flask

import ui
import api


def create_app():
    app = Flask(__name__)

    # First, pull in the environment variables called FLASK_*. This will let
    # us know if we are in a dev environment
    app.config.from_prefixed_env()

    # Always get the defaults
    app.config.from_pyfile("../default_config.py")

    # Overwrite with others if needed
    # if app.config.get("DEBUG"):
    #    app.config.from_pyfile("../default_config_dev.py")

    # Pull in the env variables again, to overwrite anything here
    app.config.from_prefixed_env()

    # Get url_for working behind SSL
    from werkzeug.middleware.proxy_fix import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

    # Set up some logging defaults based upon the config.
    # Keep the basic config at warn, so our libraries don't overwhelm us

    root = logging.getLogger()
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(name)s %(message)s", level=logging.WARN
    )
    # logging.basicConfig(level="WARN")

    logger = logging.getLogger("slideshow")
    logger.setLevel(app.config.get("LOG_LEVEL"))

    logger.info(f"Current log level: {app.config.get('LOG_LEVEL')}")

    app.register_blueprint(ui.bp)
    app.register_blueprint(api.bp)

    return app


if __name__ == "__main__":
    app = create_app()
    host = app.config.get("HOST")
    port = app.config.get("PORT")
    debug = app.config.get("DEBUG")
    app.run(host=host, port=port, debug=debug)
