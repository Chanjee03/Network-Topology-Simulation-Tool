# Network-Topology-Simulation-Tool
This Python tool parses network device configurations, detects duplicate IPs, missing configs, and link overloads, generates hierarchical network topology visualizations, simulates basic network traffic, and exports extracted data and link information to CSV files for analysis and reporting.


# Network Topology Analyzer & Simulator

A Python tool to parse network device configurations, check network health, visualize topology, simulate basic traffic, and export network data for reporting.

---

## Features

- Parse router/switch configs to extract interface IPs and masks.
- Detect duplicate IPs and missing configurations.
- Generate links, check bandwidth, and suggest load balancing.
- Visualize network topology with Graphviz and Matplotlib.
- Simulate basic network traffic (e.g., OSPF Hello, ARP Requests).
- Export extracted data and link info to CSV.

---

## Simple Steps to Use

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/network-tool.git
cd network-tool
Install dependencies:

bash
pip install pandas matplotlib graphviz networkx
Ensure Graphviz is installed on your system.

Add your configuration files to the configs/ folder.

Run the tool:

bash
python main.py
Check outputs:

output/extracted_data.csv → Extracted device/interface info.

output/links_data.csv → Links, subnets, status, bandwidth.

output/network_topology.png → Visual network topology.

Console messages for duplicate IPs, missing configs, and load balancing recommendations.

Modify or Extend
Add more devices by creating new config files.

Update parsing templates as needed.

Adjust bandwidth and expected traffic in main.py.

Author
Chandan Kumar


