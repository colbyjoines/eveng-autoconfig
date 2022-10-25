from netmiko import ConnectHandler
from netmiko import exceptions

import time

from .eve_api import EveApi
from .eve_auth import EveAuth
from .eve_topology import EveTopology
from .generate_ip_addressing import GenerateIpAddressing


class Autoconfig:
    def __init__(self, eve_config: dict) -> None:
        self._config = eve_config
        self._api = EveApi(self._config, EveAuth(self._config))
        self.topology = EveTopology(self._config["lab_path"], self._api)
        self.ip_addressing = GenerateIpAddressing(self._config, self.topology.graph)

    def configure(self):

        initial_prompt = False
        for node in self.topology.nodes:
            node_obj = self.topology.nodes[node]
            conn_params = {
                "ip": self._config["server"],
                "port": int(node_obj.port),
                "device_type": "generic_telnet",
            }

            connection = ConnectHandler(**conn_params)
            prompt = connection.read_channel_timing(2)
            if "[yes/no]" in prompt:
                connection.write_channel("no\n")
                initial_prompt = True

        if initial_prompt:
            time.sleep(10)

        for node in self.topology.nodes:
            node_obj = self.topology.nodes[node]
            conn_params = {
                "ip": self._config["server"],
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

            config_set.extend(self._config["config_options"]["additional_config"])
            config_set.append(f"router-id 0.0.0." + node_obj.id)
            config_set.append(f"network 0.0.0.0 0.0.0.0 area 0")
            connection = ConnectHandler(**conn_params)
            connection.enable()
            while True:
                try:
                    res = connection.send_config_set(config_set)
                    break
                except exceptions.ReadTimeout:
                    time.sleep(5)
                    res = connection.send_config_set(config_set)
            print(res)
