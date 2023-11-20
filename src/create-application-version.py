# Using API calls veracode for creating sandbox automatically.
import base64
from urllib import request

import requests
import urllib
import json
import sys

from veracode_api_py import Applications, Sandboxes


def get_applications_list():
    vera_app_list = Applications()
    return vera_app_list.get_app_list()


def get_app_by_name(app_name):
    vera_app = Applications()
    return vera_app.get_by_name(app_name)


def create_application_sandbox(application_guid, sandbox_name):
    app_sandbox = Sandboxes()
    app_sandbox.create(application_guid, sandbox_name)


if __name__ == "__main__":
    get_app_guid = get_app_by_name(sys.argv[1])[0]["guid"]
    create_application_sandbox(get_app_guid, sys.argv[2])
