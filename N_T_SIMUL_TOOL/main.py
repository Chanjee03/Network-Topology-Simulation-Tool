import time
import pandas as pd
import ipaddress

from parser import parse_all_configs
from t_builder import build_graphviz_topology, build_matplotlib_topology
from analyzer import check_duplicate_ips, check_missing_configs, check_capacity, recommend_load_balancing
from simulator import NetworkSimulator

# Step 1: Parse configs
data_df = parse_all_configs("configs", "templates/interface_ip.template")
print("\nExtracted Data:\n", data_df)

# Step 1a: Save extracted data to CSV
data_df.to_csv("output/extracted_data.csv", index=False)
print("\n✅ Extracted data saved to output/extracted_data.csv")

# Step 2: Build links with dummy bandwidth
def generate_links(df):
    links = []
    ip_map = {}
    for _, row in df.iterrows():
        device = row["DEVICE"]
        ip = row["IPADDR"]
        mask = row["MASK"]
        if not ip or not mask:
            continue
        try:
            subnet = str(ipaddress.ip_network(f"{ip}/{mask}", strict=False))
        except ValueError:
            continue
        if subnet not in ip_map:
            ip_map[subnet] = []
        ip_map[subnet].append((device, ip))
    for subnet, nodes in ip_map.items():
        if len(nodes) > 1:
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    dev1, ip1 = nodes[i]
                    dev2, ip2 = nodes[j]
                    links.append({
                        "Device1": dev1,
                        "Device2": dev2,
                        "Subnet": subnet,
                        "Status": "green",
                        "Bandwidth_Mbps": 100
                    })
    return links

links = generate_links(data_df)

# Step 2a: Save links to CSV
links_df = pd.DataFrame(links)
links_df.to_csv("output/links_data.csv", index=False)
print("✅ Link data saved to output/links_data.csv")

# Step 3: Checks
dupes = check_duplicate_ips(data_df)
if dupes is not None:
    print("⚠️ Duplicate IPs found:\n", dupes)

missing = check_missing_configs(data_df, ["R1", "R2", "R3", "SW1", "SW2"])
if missing is not None:
    print("⚠️ Missing configs for:", missing)

# Step 3a: Capacity check (fixed to match analyzer.py unpacking)
overloaded = check_capacity(
    [(l["Device1"], l["Device2"], l["Subnet"], l["Status"], l["Bandwidth_Mbps"]) for l in links],
    {("R1", "R3"): 200}  # Example expected traffic
)
if overloaded:
    recs = recommend_load_balancing(overloaded)
    print("\n".join(recs))

# Step 4: Topology visualization
build_graphviz_topology(
    [(l["Device1"], l["Device2"], l["Status"], l["Bandwidth_Mbps"]) for l in links],
    "output/network_topology"
)
build_matplotlib_topology(
    [(l["Device1"], l["Device2"], l["Status"], l["Bandwidth_Mbps"]) for l in links]
)

# Step 5: Day-1 Simulation
sim = NetworkSimulator()
sim.add_node("R1", "Router")
sim.add_node("R2", "Router")
sim.add_node("SW1", "Switch")
sim.start()

sim.send("R1", "R2", "OSPF Hello")
sim.send("R1", "SW1", "ARP Request")

time.sleep(3)
sim.stop()
