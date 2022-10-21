# eve-config-gen

A basic library used to generate baseline configuration for an eve-ng network topology.

Steps to configure and run eve_config_gen script:
1. Update config.json file with topology and environement details. Reference config_options section for details

```
{
  "lab_path": "Personal/script_test_02.unl",
  "server": "192.168.50.100",
  "username": "admin",
  "password": "eve",
  "config_options": {
    "nodes_to_configure": [],
    "loopback_count": 3,
    "add_duplicate_loopbacks": [],
    "private_addressing": false,
    "baseline_config": [
      "router ospf 1",
      "network 0.0.0.0 0.0.0.0 area 0"
    ]
  }
}
```
2. Connect all nodes in the topology. Do not include multiple links between nodes. Verify that the topology (or referenced nodes in config file) are Cisco routers.
3. Execute the eve_config_gen.py after installing all dependencies included in requirements.txt. **Note** that this will likely fail a few times. Run the scirpt multiple times and it will eventually complete entirely. 

## config_options

### nodes_to_configure
This is used to selectively choose the nodes in which the configuration will be applied. A default, empty list, will apply configuration to all nodes in the topology. A list, such as ['R1', 'R2'], will apply configuration to both nodes R1 and R2.

### loopback_count
This will apply a variation of loopback addressing based off of this value. A value of 3 will result the following Cisco configuration
```
interface Loopback0
 ip address 20.100.0.1 255.255.255.0
 ip ospf network point-to-point
!
interface Loopback1
 ip address 20.100.1.1 255.255.255.0
 ip ospf network point-to-point
!
interface Loopback2
 ip address 20.100.2.1 255.255.255.0
 ip ospf network point-to-point
!
interface Loopback10
 ip address 100.1.2.0 255.255.255.255
!
interface Loopback11
 ip address 100.1.2.1 255.255.255.255
!
interface Loopback12
 ip address 100.1.2.2 255.255.255.255
```
### add_duplicate_loopbacks
This value will add duplicate networks on a list of nodes. A loopback_count value of 3 will apply the following configuration on the referenced nodes
```
interface Loopback20
 ip address 1.1.1.20 255.255.255.255
 ip ospf network point-to-point
!
interface Loopback21
 ip address 1.1.1.21 255.255.255.255
 ip ospf network point-to-point
!
interface Loopback22
 ip address 1.1.1.22 255.255.255.255
 ip ospf network point-to-point
```
### private_addressing
true will result **10.1.xx.x** for physical/internode connectivity. false will result **xx.1.1.xx** for physical/internode connectivity

### baseline_config
The list of commands will be passed into the configuration script after all interface and hostname configurations are applied


### Caveats
- Nodes cannot have multiple links connecting to each node
- The initial configuration will fail if the topology is brand new and at an initial configuration prompt. Run the script multiple times and it will eventually pass
- Each node much include a prefix, followed by a number, which will be used to seed the configuration. For example "pe2" will utilize 2 as the node IP when generating inter-node addressing