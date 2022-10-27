# eveng-autoconfig

A basic library used to generate and deploy a baseline configuration to an eve-ng network topology. The script will generate and apply boilerplate IP addressing to transit links and loopback interfaces.

An outline of the scheme is as follows:
- R1 that connects to R2 will receive a transit link configuration with 10.0.**12.1**/24 applied to R1's interface that faces R2. R2 will receive a transit link configuration with 10.0.12.2/24 applied to R2's interface that faces R1. **12** being the combination of R1's ID, 1, and R2's ID, 2. Each router's transit link will utilize their ID as the host IP address on a given segment. 
- R1 that is connected to SW5 will receive a configuration 10.**5**.**5**.**1**/24. Where 5 is the switch ID and 1 is the router ID, acting as the host address on the segment.
- Multiple switches that are connected will be grouped and the lowest switch ID will be used to generate the IP scheme. Any router that connects to a group of switches will utilize the same pattern as the previous bullet, except it will utilize the lowest switch ID in a given group of connected switches. 

Steps to configure and run eve_config_gen script:
1. Update config.json file with topology, environement, and Cisco image details. Reference config_options section for details

```
{
  "lab_path": "Personal_Labs/lab_01.unl",
  "server": "10.1.1.1",
  "username": "admin",
  "password": "eve",
  "config_options": {
    "nodes_to_configure": [],
    "loopback_count": 3,
    "add_duplicate_loopbacks": [],
    "additional_config": [
      "router ospf 1", 
      "network 0.0.0.0 0.0.0.0 area 0"
    ]
  },
  "images": {
    "router_ios_01": "Router",
    "router_ios_02": "Router",
    "switch_ios_01": "Switch"
  }
}
```
2. Connect all nodes in the topology. Do not include multiple links between nodes. Verify that the topology (or referenced nodes in config file) are Cisco routers and switches.
3. Execute the eveng_autoconfig followed by the config file as an argument after installing all dependencies included in requirements.txt. **Note** that this will likely fail a few times. Run the scirpt multiple times and it will eventually complete entirely. 

```
Example
py eveng_autoconfig.py config.json
```

## config_options

### nodes_to_configure - Optional
This is used to selectively choose the nodes in which the configuration will be applied. A default, empty list, will apply configuration to all nodes in the topology. A list, such as ['R1', 'R2'], will apply configuration to both nodes R1 and R2.

### loopback_count - Required (max 9)
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
### add_duplicate_loopbacks - Optional
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

### baseline_config - Optional
The list of commands will be passed into the configuration script after all interface and hostname configurations are applied

### images - Required
Provides definition of node types (Router or Switch) that will be used for creating an IP scheme. Each dictionary key should be replaced with an image name or substring used to identify node types
```
Example
"images": {
  "iosv-": "Router",
  "iosvl2-": "Switch"
 }
```

### Caveats
- All nodes must be online and in a configurable state
- Nodes cannot have multiple links interconnecting the same nodes
- A single router cannot have multiple links connected to a single L2 segment or group of switches
- Each node name much include a prefix, followed by a unique number, which will be used to seed the configuration. For example "pe2" will utilize 2 as the node IP when generating inter-node addressing
- Switch VLANs will not be considered when generating an IP scheme
- The initial configuration may fail if the topology is brand new and at an initial configuration prompt. Run the script multiple times and it will eventually pass
