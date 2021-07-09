#!/usr/bin/env python

__version__ = "1.0"
__author__ = "omar elfarsaoui"
__twitter__ = "@omarelfarsaoui"

try:
    from requests import get
    import requests.packages.urllib3
    from bs4 import BeautifulSoup
    from termcolor import colored
    import argparse
except ModuleNotFoundError as identifier:
    print(colored("[+] {} \n[!] pip3 install module".format(str(identifier)),"red"))
    exit(0)

# disable requests warnings
requests.packages.urllib3.disable_warnings()


def initArgparse():
    parser = argparse.ArgumentParser(description='Simple tools to test jira endpoints')
    parser.add_argument("-u", "--url", help="jira instence", type=str, metavar='', required=True)
    return parser.parse_args()

def getEndPoints(version):
    """
    this function take the version as params
    and return list of endpoint specific from
    documentation for the version given
    """
    try:
        url = "https://docs.atlassian.com/software/jira/docs/api/REST/{0}/".format(version)
        req = get(url=url)
        soup = BeautifulSoup(req.content, "html.parser")

        resources = soup.findAll('div', {'class':'resource'})

        endpoints = list()

        for resource in resources:
            for method in resource.find('div', {'class':'methods'}):
                endpoint = method.find('code').text.split()
                if "}" not in endpoint[1] and endpoint[0].startswith("GET"):
                    endpoints.append(endpoint[1])
        return endpoints


    except KeyboardInterrupt:
        print(colored("[!] Ctrl+c detected", "yellow"))
        exit(0)

    except Exception as error:
        print(colored("[!] {0}".format(error), "red"))


def getJiraVersion(url):
    """
    This function get the current version running
    """
    try:

        versionUrl = "rest/api/2/serverInfo"

        if url.endswith("/"):
            url = url + versionUrl
        else:
            url = url + "/" + versionUrl

        resp = get(url=url)

        version = resp.json().get('version')

        print(colored("[+] Jira Version {}".format(version), "green"))
        return version

    except KeyboardInterrupt:
        print(colored("[!] Ctrl+c detected", "yellow"))
        exit(0)

    except Exception as identifier:
        print(colored("[!] Unable to get the version \n[!] may be is not jira instance", "red"))
        exit(0)

def makeReqToJira(url, endpoints):
    """
    this fuction take url and enpoints as list 
    and request to every enpoint
    """
    try:
        if url.endswith("/"):
            url = url[:-1]

        for endpoint in endpoints:
            jiraRestApi = url + endpoint
            response = get(jiraRestApi)
            statusCode = response.status_code
            result = "{} {} {}".format(statusCode, response.headers.get('content-length'), response.url)

            if statusCode == 200:
                print(colored("[+] {} ".format(result), "green"))
            elif statusCode == 401:
                print(colored("[-] {} ".format(result), "red"))
            else:
                print(colored("[!] {} ".format(result), "blue"))
            
    except KeyboardInterrupt:
        print(colored("[!] Ctrl+c detected", "yellow"))
        exit(0)

    except Exception as error:
        print(colored("[!] {0}".format(error), "red"))

def main(url):
    try:

        version = getJiraVersion(url)
        endpoints = getEndPoints(version=version)
        makeReqToJira(url=url, endpoints=endpoints)

    except KeyboardInterrupt:
        print(colored("[!] Ctrl+c detected", "yellow"))
        exit(0)

    except Exception as error:
        print(colored("[!] {0}".format(error), "red"))


if __name__ == "__main__":
    args = initArgparse()
    main(args.url)
    