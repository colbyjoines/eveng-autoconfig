from cgi import print_directory
from distutils.command.config import config
import json
from os import link
from netmiko import ConnectHandler
from ipaddress import IPv4Address
from numpy import append
import requests
import time
import re

from get_lab import get_nodes, get_topology
from get_auth import get_auth


with open("config.json") as json_file:
    data = json.load(json_file)

cookies = get_auth().cookies
nodes = get_nodes(cookies)
topology = get_topology(cookies)

for index, node in enumerate(nodes):
    if (
        data["config_options"]["nodes_to_configure"]
        and nodes[node]["name"] not in data["config_options"]["nodes_to_configure"]
    ):
        continue

    port = nodes[node]["url"].split(":")[2]
    node_interfaces = []
    interface = {}
    destination_nodes = []
    for links in topology:
        source_node_number = re.findall(r"\d+", links["source_node_name"])[0]
        destination_node_number = re.findall(r"\d+", links["destination_node_name"])[0]
        if links["source_node_name"] == nodes[node]["name"]:
            if source_node_number < destination_node_number:
                interface = links
                if data["config_options"]["private_addressing"]:
                    interface["ip_address"] = f"10.1.{source_node_number}{destination_node_number}.{source_node_number}"
                else:    
                    interface["ip_address"] = f"{source_node_number}{destination_node_number}.1.1.{source_node_number}"
            else:
                interface = links
                if data["config_options"]["private_addressing"]:
                    interface["ip_address"] = f"10.1.{destination_node_number}{source_node_number}.{source_node_number}"
                else:    
                    interface["ip_address"] = f"{destination_node_number}{source_node_number}.1.1.{source_node_number}"

            node_interfaces.append(
                {
                    "ip_address": interface["ip_address"],
                    "interface_id": links["source_label"],
                }
            )

            destination_nodes.append(links["destination_node_name"])

        elif links["destination_node_name"] == nodes[node]["name"]:
            if destination_node_number < source_node_number:
                interface = links
                if data["config_options"]["private_addressing"]:
                    interface["ip_address"] = f"10.1.{destination_node_number}{source_node_number}.{destination_node_number}"
                else:    
                    interface["ip_address"] = f"{destination_node_number}{source_node_number}.1.1.{destination_node_number}"
                node_interfaces.append(
                    {
                        "ip_address": interface["ip_address"],
                        "interface_id": links["destination_label"],
                    }
                )
                destination_nodes.append(links["source_node_name"])

    conn_params = {
        "ip": data["server"],
        "port": int(port),
        "device_type": "cisco_ios_telnet",
    }


    config_set = ["hostname " + nodes[node]["name"]]

    node_number = re.findall(r"\d+", nodes[node]["name"])[0]
    for interface in node_interfaces:
        config_set.append("interface " + interface["interface_id"])
        config_set.append("ip address " + interface["ip_address"] + " 255.255.255.0")
        config_set.append("no shut")

    for loopback in range(0, data["config_options"]["loopback_count"]):
        config_set.append(f"interface lo{str(loopback)}")
        config_set.append(
            f"ip address "
            + node_number
            + f"0.100.{str(loopback)}.1 255.255.255.0"
        )
        config_set.append(f"ip ospf network point-to-point")
        config_set.append(f"interface lo{str(loopback + 10)}")
        config_set.append(
            f"ip address 100.1.{node_number}.{str(loopback)} 255.255.255.255"
        )
        if nodes[node]["name"] in data["config_options"]["add_duplicate_loopbacks"]:
            loopback = str(loopback + 20)
            config_set.append(f"interface lo{loopback}")
            config_set.append(f"ip address 1.1.1.{loopback} 255.255.255.255")
            config_set.append(f"ip ospf network point-to-point")

    config_set.extend(data["config_options"]["baseline_config"])
    connection = ConnectHandler(**conn_params)
    
    print(config_set)
    if "no" in connection.find_prompt():
        resp = connection.send_command("no")
        print(resp)
        time.sleep(5)

    connection.enable()
    config_resp = connection.send_config_set(config_set)
    print(config_resp)
 
    
