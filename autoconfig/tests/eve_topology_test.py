import unittest
import json

from ..eve_api import EveApi
from ..eve_auth import EveAuth
from ..eve_topology import EveTopology
from ..generate_ip_addressing import GenerateIpAddressing
from ..autoconfig import Autoconfig

class AutoconfigTest(unittest.TestCase):
    def setUp(self) -> None:
        self.config = json.load(open("config.json"))

    
    def test_get_nodes(self):
        obj = Autoconfig(self.config)
