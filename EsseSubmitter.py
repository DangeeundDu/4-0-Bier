from attack import Submitter, SubmittableFlags, NoFlag
from json import loads
import requests


class EsseSubmitter(Submitter):
    bearer: str = "eyJhbGciOiJIUzUxMiJ9.eyJyb2xlcyI6IlJPTEVfU1RVREVOVCxST0xFX1RFQU0wOCIsInRlYW1JZCI6OCwic3ViIjoiZTEyMDIxMTUyIiwiaWF0IjoxNjU0MzI3ODM2LCJleHAiOjE2NTQ0MTQyMzZ9.HCMFjdJvzwcTcDajL07GtcFRMT3rp4EzjtBet7Dwp-_Umq-BdcAXs6u9KYdF-327QOZYw-D2PC5XADwCIGYSiA"
    server = "10.10.40.200"
    port = "443"
    url = f"https://{server}:{port}/api/flags"
    headers = {
        "accept": "*/*",
        "Authorization": f"Bearer {bearer}",
        "Content-Type": "application/json",
    }

    def __call__(self, flags: SubmittableFlags):
        data = {
            "data": [flag for flag in flags if type(flag) != NoFlag]
        }

        resp = loads(requests.post(self.url, headers=self.headers, json=data, verify=False).text)

        for flag, result in [x.values() for x in resp["data"]]:
            if result != "OK":
                print(f"ERROR: submitting flag [{flag}] failed. Result: [{result}]")
            elif result == "OK":
                print("OK Flag")
