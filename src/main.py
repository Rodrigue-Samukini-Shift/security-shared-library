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


def get_findings(application_guid, sandbox_guid, type):
    finding = Findings()
    app_findings = finding.get_findings(application_guid, type, 'TRUE', None, sandbox_guid)
    return app_findings


def pipeline_status(sorted_vulns):
    if sorted_vulns["Very High"] + sorted_vulns["High"] + sorted_vulns["Medium"] + sorted_vulns["Low"] + \
            sorted_vulns["Very Low"] + sorted_vulns["Information"] > 0:
        print("*******************************************************************")
        print("       THE PIPELINE FAILED DUE TO SAST VULNERABILITIES FOUND       ")
        print("*******************************************************************")
        return sys.exit(1)
    else:
        print("*******************************************************************")
        print("           SUCCESSFUL SAST SCAN - NO VULNERABILITIES FOUND         ")
        print("*******************************************************************")
        return sys.exit(0)



def sast_passfail_policies(application_guid, sandbox_guid):
    issues = get_findings(application_guid, sandbox_guid, 'STATIC')
    sorted_vulns = count_vulns_by_severity(issues)
    affichage(sorted_vulns, 13)
    pipeline_status(sorted_vulns)

def sca_passfail_policies(application_guid, sandbox_guid):
    issues = get_findings(application_guid, sandbox_guid, 'SCA')
    return issues


def affichage(sorted_vulns: dict, space):
    print(" ************************ THE VERACODE VUNERABILITY RESULT ***************************")
    print(" ")
    print("                COUNT   ")
    for elem in sorted_vulns:
        nbr_print = space - len(elem)
        to_print = " " * nbr_print + elem + ":" + " " * 3 + str(sorted_vulns[elem])
        print(to_print)


def count_vulns_by_severity(issues):
    results = {"Very High": 0, "High": 0, "Medium": 0, "Low": 0, "Very Low": 0, "Information": 0}
    for vuln in issues:
        if vuln["finding_details"]["severity"] == 5:
            results["Very High"] += 1
        if vuln["finding_details"]["severity"] == 4:
            results["High"] += 1
        if vuln["finding_details"]["severity"] == 3:
            results["Medium"] += 1
        if vuln["finding_details"]["severity"] == 2:
            results["Low"] += 1
        if vuln["finding_details"]["severity"] == 1:
            results["Very Low"] += 1
        if vuln["finding_details"]["severity"] == 0:
            results["Information"] += 1
    return results


if __name__ == "__main__":
    get_app_guid = get_app_by_name(sys.argv[1])[0]["guid"]
    if sys.argv[3] == "create":
        sandbox_created = create_application_sandbox(get_app_guid, sys.argv[2])
    else:
        sandbox_uid = get_sandbox_uid(get_app_guid, sys.argv[2])
        #sast_passfail_policies(get_app_guid, sandbox_uid)
        sca_passfail_policies(get_app_guid, sandbox_uid)
