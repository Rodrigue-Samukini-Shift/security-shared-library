#Using API calls veracode for creating sandbox automatically.
import request
import urllib3
def create_application_sandboxe(veracode_url, veracode_id, veracode_key, application):
    url = "{0}/appsec/v1/applications/{1}/sandboxes".format(veracode_url, application)
    payload = {"custom_fields": [{"name": "string", "value": "string"}], "name": "string", "auto_recreate": false}
