import json
import os
try:
    from urllib.parse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

import requests
from requests.auth import HTTPBasicAuth
from util.config import config

try:
    import urllib3
    urllib3.disable_warnings()
except (AttributeError, ImportError):
    pass

class Cuckoo():

    def __init__(self, config):
        self.url_base = config.get("cuckoo_url_base")
        self.api_user = config.get("cuckoo_user")
        self.api_passwd = config.get("cuckoo_passwd")
        self.cuckoo_force = config.get("cuckoo_force")

    def upload(self, path, name):

        if self.cuckoo_force or self.cuckoo_check_if_dup(os.path.basename(path)) is False:
            print("Sending file to Cuckoo")
            self.postfile(path, name)

    def cuckoo_check_if_dup(self, sha256):
        """
        Check if file already was analyzed by cuckoo
        """
        try:
            print(("Looking for tasks for: {}".format(sha256)))
            res = requests.get(urljoin(self.url_base, "/files/view/sha256/{}".format(sha256)),
                verify=False,
                auth=HTTPBasicAuth(self.api_user,self.api_passwd),
                timeout=60)
            if res and res.ok and res.status_code == 200:
                print(("Sample found in Sandbox, with ID: {}".format(res.json().get("sample", {}).get("id", 0))))
                return True
            else:
                return False
        except Exception as e:
            print(e)

        return False

    def postfile(self, artifact, fileName):
        """
        Send a file to Cuckoo
        """
        files = {"file": (fileName, open(artifact, "rb").read())}
        try:
            res = requests.post(urljoin(self.url_base, "tasks/create/file").encode("utf-8"), files=files, auth=HTTPBasicAuth(
                            self.api_user,
                            self.api_passwd
                        ),
                        verify=False)
            if res and res.ok:
                print(("Cuckoo Request: {}, Task created with ID: {}".format(res.status_code, res.json()["task_id"])))
            else:
                print(("Cuckoo Request failed: {}".format(res.status_code)))
        except Exception as e:
            print(("Cuckoo Request failed: {}".format(e)))
        return


    def posturl(self, scanUrl):
        """
        Send a URL to Cuckoo
        """
        data = {"url": scanUrl}
        try:
            res = requests.post(urljoin(self.url_base, "tasks/create/url").encode("utf-8"), data=data, auth=HTTPBasicAuth(
                            self.api_user,
                            self.api_passwd
                        ),
                        verify=False)
            if res and res.ok:
                print(("Cuckoo Request: {}, Task created with ID: {}".format(res.status_code, res.json()["task_id"])))
            else:
                print(("Cuckoo Request failed: {}".format(res.status_code)))
        except Exception as e:
            print(("Cuckoo Request failed: {}".format(e)))
        return
