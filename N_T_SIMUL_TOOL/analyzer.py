import pandas as pd
import ipaddress

def check_duplicate_ips(df):
    duplicates = df[df.duplicated(subset=["IPADDR"], keep=False)]
    return duplicates if not duplicates.empty else None

def check_missing_configs(df, expected_devices):
    found_devices = set(df["DEVICE"].unique())
    missing = set(expected_devices) - found_devices
    return missing if missing else None

def check_vlan_issues(df):
    # TODO: Extend with VLAN parsing template
    return None

def check_gateways(df):
    # Simple heuristic: router interface should not be .0 or .255
    bad_gws = df[df["IPADDR"].str.endswith(".0") | df["IPADDR"].str.endswith(".255")]
    return bad_gws if not bad_gws.empty else None

def check_capacity(links, traffic_matrix):
    """Compare traffic demand vs link capacity."""
    overloaded = []
    for dev1, dev2, subnet, color, bw in links:
        demand = traffic_matrix.get((dev1, dev2), 0)
        if demand > bw:
            overloaded.append((dev1, dev2, demand, bw))
    return overloaded

def recommend_load_balancing(overloaded_links):
    recs = []
    for dev1, dev2, demand, bw in overloaded_links:
        recs.append(f"🔴 Link {dev1} ↔ {dev2} overloaded ({demand} > {bw}). Suggest secondary path or load balancing.")
    return recs
