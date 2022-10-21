# eve-config-gen

A basic library used to generate baseline configuration for an eve-ng network topology.

Steps to configure and run eve_config_gen script:
1. Update config.json file with topology and environement details

```
{
  "lab_path": "Personal/script_test_02.unl",
  "server": "192.168.50.100",
  "username": "admin",
  "password": "eve",
  "config_options": {
    "nodes_to_configure": [],
    "loopback_count": 10,
    "add_duplicate_loopbacks": ["R4", "R5"],
    "private_addressing": true,
    "baseline_config": [
      "router ospf 1",
      "network 0.0.0.0 0.0.0.0 area 0"
    ]
  }
}
```