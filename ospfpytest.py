from nornir_scrapli.tasks import netconf_get
from xml.dom import minidom


def get_state(task):
    result = task.run(task=netconf_get, filter_="//ospf-neighbor", filter_type="xpath")
    resulter = result.result
    neighbors = minidom.parseString(resulter).getElementsByTagName("state")
    for neighbor in neighbors:
        state = neighbor.firstChild.nodeValue
        return state


def count_neighbors(task):
    result = task.run(task=netconf_get, filter_="//ospf-neighbor", filter_type="xpath")
    resulter = result.result
    neighbors = minidom.parseString(resulter).getElementsByTagName("neighbor-id")
    num_neighbors = len(neighbors)
    return num_neighbors


def test_ospf(nr):
    state_result = nr.run(task=get_state)
    count_result = nr.run(task=count_neighbors)
    for host in nr.inventory.hosts.values():
        state = state_result[f"{host}"][0].result
        assert state == "ospf-nbr-full"
        count = count_result[f"{host}"][0].result
        assert count == 2
