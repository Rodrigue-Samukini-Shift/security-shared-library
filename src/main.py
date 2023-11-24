# Using API calls veracode for creating sandbox automatically.
import base64
from urllib import request

import requests
import urllib
import json
import sys

from veracode_api_py import Applications, Sandboxes, Findings


def get_applications_list():
    vera_app_list = Applications()
    return vera_app_list.get_app_list()


def get_app_by_name(app_name):
    vera_app = Applications()
    return vera_app.get_by_name(app_name)


def get_sandbox_uid(application_guid, sandbox_name):
    app_sandbox = Sandboxes()
    app_exists_sandbox = app_sandbox.get_all(application_guid)
    for sand in app_exists_sandbox:
        if sand["name"] == sandbox_name:
            print("Sandbox " + sandbox_name + " already exists...")
            return sand["guid"]


def create_application_sandbox(application_guid, sandbox_name):
    app_sandbox = Sandboxes()
    app_exists_sandbox = app_sandbox.get_all(application_guid)
    for sand in app_exists_sandbox:
        if sand["name"] == sandbox_name:
            print("Sandbox " + sandbox_name + " already exists...")
            return sand["guid"]
    create_new = app_sandbox.create(application_guid, sandbox_name)
    print("Sandbox " + sandbox_name + " successful created...")
    return create_new["guid"]


def get_findings(application_guid, sandbox_guid):
    finding = Findings()
    app_findings = finding.get_findings(application_guid, 'STATIC', 'TRUE', None, sandbox_guid)
    return app_findings


def sast_passfail_policies():
    return 0


if __name__ == "__main__":
    get_app_guid = get_app_by_name(sys.argv[1])[0]["guid"]
    if sys.argv[2] == "created":
        sandbox_created = create_application_sandbox(get_app_guid, sys.argv[2])
    else:
        sandbox_uid = get_sandbox_uid(get_app_guid, sys.argv[2])
        get_findings(get_app_guid, sandbox_uid)
