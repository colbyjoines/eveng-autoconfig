from netmiko import ConnectHandler
from netmiko import exceptions

import time

from pprint import pprint

from .eve_api import EveApi
from .eve_auth import EveAuth
from .eve_topology import EveTopology
from .generate_ip_addressing import GenerateIpAddressing


class Autoconfig:
    def __init__(self, eve_config: dict) -> None:
        self.config = eve_config
        self.api = EveApi(self.config, EveAuth(self.config))
        self.topology = EveTopology(self.config, self.api)
        self.ip_addressing = GenerateIpAddressing(self.config, self.topology.graph)
        pprint(self.ip_addressing.addressing)

    def configure(self):

        initial_prompt = False
        for node in self.topology.nodes:
            node_obj = self.topology.nodes[node]
            conn_params = {
                "ip": self.config["server"],
                "port": int(node_obj.port),
                "device_type": "generic_telnet",
            }
            print("Checking " + node_obj.name + "for initial prompt")
            connection = ConnectHandler(**conn_params)
            prompt = connection.read_channel_timing(2)
            if "[yes/no]" in prompt:
                print("Initial prompt found on node " + node_obj.name)
                connection.write_channel("no\n")
                initial_prompt = True

        if initial_prompt:
            time.sleep(10)

        for node in self.topology.nodes:
            node_obj = self.topology.nodes[node]
            conn_params = {
                "ip": self.config["server"],
                "port": int(node_obj.port),
                "device_type": "cisco_ios_telnet",
            }

            config_set = [
                "hostname " + node_obj.name,
            ]

            if node_obj.node_type == "Router":
                for interface in self.ip_addressing.addressing[node_obj.name]:
                    config_set.append("interface " + interface["interface"])
                    config_set.append(
                        "ip address " + interface["address"] + " " + interface["mask"]
                    )
                    config_set.append("no shut")
                    config_set.extend(interface["additional_config"])

            config_set.extend(self.config["config_options"]["additional_config"])
            config_set.append(f"router-id 0.0.0." + node_obj.id)
            config_set.append(f"network 0.0.0.0 0.0.0.0 area 0")
            connection = ConnectHandler(**conn_params)
            connection.enable()
            while True:
                try:
                    res = connection.send_config_set(config_set)
                    break
                except exceptions.ReadTimeout or ValueError:
                    time.sleep(5)
                    res = connection.send_config_set(config_set)
                    break
            print(res)
