from xml.dom import minidom
from nornir_scrapli.tasks import netconf_get

def random(task):
    result = task.run(task=netconf_get, filter_= "/native/version", filter_type="xpath")
    resulter = result.result
    vers = minidom.parseString(resulter).getElementsByTagName("version")
    for ver in vers:
        version = ver.firstChild.nodeValue
        return version

def test_version(nr):
    result = nr.run(task=random)
    for host in nr.inventory.hosts.values():
        version = result[f"{host}"][0].result
        assert version == "16.11"
